"""
encoding.py
-----------
Converts the Student model's text (categorical) fields into numbers so
the recommendation model can use them — this is the "encoding" step of
the ML pipeline.

Example (label encoding, what this module does):

    Branch   ->  CSE=0, ISE=1        (alphabetical order of the unique values)
    Learning Style -> Auditory=0, Reading=1, Visual=2
    Career Goal -> AI Engineer=0, Data Analyst=1, Web Developer=2

Why LabelEncoder and not one-hot here: `learning_style`/`branch`/
`career_goal` each have a small, open-ended set of values that will grow
as more students sign up (a new branch, a new career goal). LabelEncoder
gives one compact integer column per field, so a new category doesn't
change the model's feature count — it just needs re-fitting. The
trade-off: it implies a false ordering (Visual=2 is not "more" than
Reading=1). For a tree-based model (Random Forest / Gradient Boosting)
this doesn't hurt much because trees split on thresholds rather than
assuming a linear relationship. If you later switch to a linear model
(Logistic Regression) or want to be strict about it, one-hot encode
these same columns instead — see `one_hot_encode_dataframe` below.

Encoders are fit once on the current student population and saved to
disk (joblib) so that encoding stays *consistent* between training and
inference — a new prediction request must map "CSE" to the same integer
the model was trained on, not a freshly-refit one.
"""

import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
ENCODERS_PATH = os.path.join(ARTIFACT_DIR, "label_encoders.joblib")

# The single-valued categorical fields on Student that need encoding.
CATEGORICAL_COLUMNS = ["degree", "branch", "interests", "learning_style", "career_goal"]

UNSEEN_LABEL_CODE = -1  # code assigned to a category the encoder never saw during fit


def fit_label_encoders(df: pd.DataFrame, columns=CATEGORICAL_COLUMNS) -> dict:
    """Fit one LabelEncoder per categorical column on the given DataFrame.
    Returns {column_name: fitted LabelEncoder}."""
    encoders = {}
    for col in columns:
        le = LabelEncoder()
        # LabelEncoder can't handle NaN -- treat missing category as its own label
        values = df[col].fillna("Unknown").astype(str)
        le.fit(values)
        encoders[col] = le
    return encoders


def save_encoders(encoders: dict, path: str = ENCODERS_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(encoders, path)


def load_encoders(path: str = ENCODERS_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No fitted encoders found at {path}. Run fit_and_save_encoders() first."
        )
    return joblib.load(path)


def _safe_transform(le: LabelEncoder, values: pd.Series) -> pd.Series:
    """Transform values with a fitted LabelEncoder, mapping any category
    the encoder never saw during fit to UNSEEN_LABEL_CODE instead of
    raising. This matters at inference time: a new student might report a
    branch or career goal that didn't exist in the training data."""
    known = set(le.classes_)
    return values.apply(lambda v: int(le.transform([v])[0]) if v in known else UNSEEN_LABEL_CODE)


def encode_dataframe(df: pd.DataFrame, encoders: dict, columns=CATEGORICAL_COLUMNS,
                       keep_original=True) -> pd.DataFrame:
    """Apply fitted encoders to a DataFrame. Adds `<col>_encoded` columns;
    set keep_original=False to drop the original text columns instead."""
    df = df.copy()
    for col in columns:
        values = df[col].fillna("Unknown").astype(str)
        df[f"{col}_encoded"] = _safe_transform(encoders[col], values)
        if not keep_original:
            df = df.drop(columns=[col])
    return df


def encode_single_student(student: dict, encoders: dict, columns=CATEGORICAL_COLUMNS) -> dict:
    """Encode one student's categorical fields for a live prediction
    request, e.g. {"branch": "CSE", "learning_style": "Visual", ...}
    -> {"branch_encoded": 0, "learning_style_encoded": 2, ...}"""
    encoded = {}
    for col in columns:
        raw_value = str(student.get(col) or "Unknown")
        encoded[f"{col}_encoded"] = int(
            _safe_transform(encoders[col], pd.Series([raw_value])).iloc[0]
        )
    return encoded


def decode_value(column: str, code: int, encoders: dict):
    """Reverse an encoded integer back to its original text label
    (e.g. to turn a predicted learning_path code back into a readable
    string). Returns None for the UNSEEN_LABEL_CODE sentinel."""
    if code == UNSEEN_LABEL_CODE:
        return None
    return encoders[column].inverse_transform([code])[0]


def fit_and_save_encoders(df: pd.DataFrame, columns=CATEGORICAL_COLUMNS, path: str = ENCODERS_PATH) -> dict:
    encoders = fit_label_encoders(df, columns)
    save_encoders(encoders, path)
    return encoders


# ---------------------------------------------------------------------
# Alternative: one-hot encoding
# ---------------------------------------------------------------------
def one_hot_encode_dataframe(df: pd.DataFrame, columns=CATEGORICAL_COLUMNS) -> pd.DataFrame:
    """Alternative to label encoding: expands each category into its own
    0/1 column (e.g. branch_CSE, branch_ISE). No false ordering implied,
    at the cost of more columns and needing to re-align columns whenever
    a brand-new category shows up at inference time. Prefer this if you
    move to a linear/logistic model instead of a tree-based one."""
    return pd.get_dummies(df, columns=columns, prefix=columns)
