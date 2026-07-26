"""
encoding.py
-----------
Converts text (categorical) fields into numbers so the recommendation
model can use them. Three different kinds of categorical data show up
in this project, and they each need a different encoding:

1. NOMINAL fields — one category per record, no inherent order.
   Student: degree, branch, learning_style, career_goal
   Course:  domain (the subject area, e.g. "AI", "Web Development")
   These use LABEL ENCODING (0, 1, 2... assigned alphabetically).
   Example: branch -> CSE=0, ISE=1

2. ORDINAL fields — one category per record, but with a real ranking.
   Course: difficulty (Beginner < Intermediate < Advanced)
   These use ORDINAL ENCODING with an EXPLICIT order you define, not
   alphabetical order. Alphabetically "Advanced" < "Beginner" 
   "Intermediate", which would tell the model Advanced=0 is the easiest
   level -- backwards from reality. So difficulty is mapped by hand:
       Beginner=0, Intermediate=1, Advanced=2

3. MULTI-LABEL fields — a record can hold SEVERAL values at once.
   Student: interests (e.g. "AI, Python, Machine Learning")
   LabelEncoder is the wrong tool here: it would treat "AI, Python" and
   "AI, Python, Machine Learning" as two totally unrelated categories,
   with zero connection to a student whose interests is just "AI". This
   uses MULTI-LABEL BINARIZATION instead: the comma-separated string is
   split into individual labels, and each becomes its own 0/1 column
   (interests_AI, interests_Python, interests_MachineLearning, ...). A
   student interested in AI and Python gets a 1 in both columns -- the
   overlap with other AI-only or Python-only students is preserved. If
   `interests` turns out to only ever hold a single value per student in
   practice, this still works correctly -- it just becomes equivalent to
   one-hot encoding, so there's no downside to using it defensively.

The nominal and ordinal encoders share one fit/transform/inverse_transform
interface, so encode_dataframe / encode_single_record / decode_value work
identically for both. Multi-label columns produce a variable number of
output columns instead of one, so they go through their own functions
(encode_multilabel_dataframe / encode_single_record_multilabel) — see the
usage example at the bottom of this file.
"""

import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import joblib

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
ENCODERS_PATH = os.path.join(ARTIFACT_DIR, "encoders.joblib")

# ---- Nominal fields (label-encoded, no natural order, one value per record) ----
STUDENT_NOMINAL_COLUMNS = ["degree", "branch", "learning_style", "career_goal"]
COURSE_NOMINAL_COLUMNS = ["domain"]  # the course "subject"

# ---- Ordinal fields (encoded with an explicit, hand-picked order) ----
ORDINAL_COLUMN_ORDERS = {
    "difficulty": ["Beginner", "Intermediate", "Advanced"],
}

# ---- Multi-label fields (a record can have several values at once) ----
STUDENT_MULTI_LABEL_COLUMNS = ["interests"]
MULTI_LABEL_DELIMITER = ","

UNSEEN_LABEL_CODE = -1  # code assigned to a nominal/ordinal category the encoder never saw during fit


class OrdinalCategoryEncoder:
    """Same fit/transform/inverse_transform interface as sklearn's
    LabelEncoder, but the code assigned to each category comes from an
    explicit rank order you supply, not alphabetical sorting."""

    def __init__(self, order):
        self.classes_ = list(order)  # kept as `classes_` to match LabelEncoder's API
        self._index = {v: i for i, v in enumerate(self.classes_)}

    def fit(self, values):
        unknown = set(values) - set(self.classes_)
        if unknown:
            print(f"Warning: values not in the defined order will be treated as "
                  f"unseen: {unknown}")
        return self

    def transform(self, values):
        return [self._index.get(v, UNSEEN_LABEL_CODE) for v in values]

    def inverse_transform(self, codes):
        return [self.classes_[c] if 0 <= c < len(self.classes_) else None for c in codes]


# ---------------------------------------------------------------------
# Nominal + ordinal encoding (single value per record)
# ---------------------------------------------------------------------
def fit_encoders(df: pd.DataFrame, nominal_columns=None, ordinal_columns=None) -> dict:
    """Fit one encoder per column -- LabelEncoder for nominal_columns,
    OrdinalCategoryEncoder for ordinal_columns (using the predefined
    order in ORDINAL_COLUMN_ORDERS). Returns {column_name: fitted encoder}."""
    nominal_columns = nominal_columns or []
    ordinal_columns = ordinal_columns or []
    encoders = {}

    for col in nominal_columns:
        le = LabelEncoder()
        values = df[col].fillna("Unknown").astype(str)
        le.fit(values)
        encoders[col] = le

    for col in ordinal_columns:
        order = ORDINAL_COLUMN_ORDERS[col]
        values = df[col].fillna("Unknown").astype(str)
        enc = OrdinalCategoryEncoder(order)
        enc.fit(values)
        encoders[col] = enc

    return encoders


def _safe_transform(encoder, values: pd.Series) -> pd.Series:
    """Transform values with a fitted encoder, mapping any category the
    encoder never saw during fit (nominal) or that isn't in the defined
    order (ordinal) to UNSEEN_LABEL_CODE instead of raising."""
    known = set(encoder.classes_)
    return values.apply(lambda v: int(encoder.transform([v])[0]) if v in known else UNSEEN_LABEL_CODE)


def encode_dataframe(df: pd.DataFrame, encoders: dict, columns=None, keep_original=True) -> pd.DataFrame:
    """Apply fitted nominal/ordinal encoders to a DataFrame. Adds
    `<col>_encoded` columns; set keep_original=False to drop the
    original text columns instead. Do not pass multi-label columns here
    -- use encode_multilabel_dataframe for those."""
    df = df.copy()
    columns = columns or list(encoders.keys())
    for col in columns:
        values = df[col].fillna("Unknown").astype(str)
        df[f"{col}_encoded"] = _safe_transform(encoders[col], values)
        if not keep_original:
            df = df.drop(columns=[col])
    return df


def encode_single_record(record: dict, encoders: dict, columns=None) -> dict:
    """Encode one record's nominal/ordinal fields for a live prediction
    request, e.g. {"branch": "CSE", "difficulty": "Advanced", ...}
    -> {"branch_encoded": 0, "difficulty_encoded": 2, ...}"""
    columns = columns or list(encoders.keys())
    encoded = {}
    for col in columns:
        if col not in encoders:
            continue
        raw_value = str(record.get(col) or "Unknown")
        encoded[f"{col}_encoded"] = int(
            _safe_transform(encoders[col], pd.Series([raw_value])).iloc[0]
        )
    return encoded


def decode_value(column: str, code: int, encoders: dict):
    """Reverse an encoded integer back to its original text label.
    Returns None for the UNSEEN_LABEL_CODE sentinel."""
    if code == UNSEEN_LABEL_CODE:
        return None
    return encoders[column].inverse_transform([code])[0]


# ---------------------------------------------------------------------
# Multi-label encoding (several values per record, e.g. interests)
# ---------------------------------------------------------------------
def parse_multi_label(value) -> list:
    """'AI, Python, Machine Learning' -> ['AI', 'Python', 'Machine Learning'].
    Missing/empty values -> []."""
    if value is None or (isinstance(value, float) and pd.isna(value)) or not str(value).strip():
        return []
    return [v.strip() for v in str(value).split(MULTI_LABEL_DELIMITER) if v.strip()]


def fit_multilabel_encoders(df: pd.DataFrame, columns=STUDENT_MULTI_LABEL_COLUMNS) -> dict:
    """Fit one MultiLabelBinarizer per multi-label column. Returns
    {column_name: fitted MultiLabelBinarizer}."""
    encoders = {}
    for col in columns:
        parsed = df[col].apply(parse_multi_label)
        mlb = MultiLabelBinarizer()
        mlb.fit(parsed)
        encoders[col] = mlb
    return encoders


def encode_multilabel_dataframe(df: pd.DataFrame, encoders: dict,
                                  columns=STUDENT_MULTI_LABEL_COLUMNS, keep_original=True) -> pd.DataFrame:
    """Expand each multi-label column into one 0/1 column per label seen
    during fit, e.g. interests -> interests_AI, interests_Python, ...
    Labels not seen during fit are silently dropped (no UNSEEN sentinel
    here -- a student can simply have zero known interests encoded)."""
    df = df.copy()
    for col in columns:
        mlb = encoders[col]
        known = set(mlb.classes_)
        parsed = df[col].apply(lambda v: [label for label in parse_multi_label(v) if label in known])
        encoded = mlb.transform(parsed)
        encoded_cols = pd.DataFrame(
            encoded, columns=[f"{col}_{cls}" for cls in mlb.classes_], index=df.index
        )
        df = pd.concat([df, encoded_cols], axis=1)
        if not keep_original:
            df = df.drop(columns=[col])
    return df


def encode_single_record_multilabel(record: dict, encoders: dict, columns=STUDENT_MULTI_LABEL_COLUMNS) -> dict:
    """Encode one record's multi-label field(s) for a live prediction
    request, e.g. {"interests": "AI, Python"}
    -> {"interests_AI": 1, "interests_Python": 1, "interests_Web": 0, ...}"""
    encoded = {}
    for col in columns:
        if col not in encoders:
            continue
        mlb = encoders[col]
        known = set(mlb.classes_)
        labels = [l for l in parse_multi_label(record.get(col)) if l in known]
        vec = mlb.transform([labels])[0]
        for cls, val in zip(mlb.classes_, vec):
            encoded[f"{col}_{cls}"] = int(val)
    return encoded


def decode_multilabel_value(column: str, encoded_record: dict, encoders: dict) -> list:
    """Reverse a set of interests_<label> 0/1 fields back into a list of
    label strings, e.g. {"interests_AI": 1, "interests_Web": 0} -> ["AI"]."""
    mlb = encoders[column]
    return [cls for cls in mlb.classes_ if encoded_record.get(f"{column}_{cls}") == 1]


# ---------------------------------------------------------------------
# Combined fit + save across all three encoding types
# ---------------------------------------------------------------------
def fit_and_save_encoders(student_df: pd.DataFrame = None, course_df: pd.DataFrame = None,
                            path: str = ENCODERS_PATH) -> dict:
    """Fit encoders for whichever DataFrames you pass in (student,
    course, or both) and save them together in one artifact so a single
    load_encoders() call has everything downstream code needs. Student
    fields are split automatically: nominal fields use LabelEncoder,
    `interests` uses MultiLabelBinarizer. Course fields: `domain` uses
    LabelEncoder, `difficulty` uses the ordinal encoder."""
    encoders = {}
    if student_df is not None:
        encoders.update(fit_encoders(student_df, nominal_columns=STUDENT_NOMINAL_COLUMNS))
        encoders.update(fit_multilabel_encoders(student_df, columns=STUDENT_MULTI_LABEL_COLUMNS))
    if course_df is not None:
        encoders.update(fit_encoders(course_df, nominal_columns=COURSE_NOMINAL_COLUMNS,
                                       ordinal_columns=list(ORDINAL_COLUMN_ORDERS.keys())))
    save_encoders(encoders, path)
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


# ---------------------------------------------------------------------
# Alternative: one-hot encoding (for single-valued nominal columns only
# -- never use one-hot on `difficulty`, it throws away the order; never
# use it on `interests`, it isn't set up for multi-valued strings)
# ---------------------------------------------------------------------
def one_hot_encode_dataframe(df: pd.DataFrame, columns) -> pd.DataFrame:
    return pd.get_dummies(df, columns=columns, prefix=columns)
