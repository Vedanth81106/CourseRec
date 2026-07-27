"""
train_model.py
---------------
Trains the course recommendation model.

======================================================================
PREDICTION TARGET: course `domain`, not course_id or course_name.
======================================================================
Reasoning (see also the longer version in the project README/chat):
  - course_id / course_name are arbitrary, high-cardinality labels with
    no shared structure. A new course has zero training examples and
    can never be predicted; existing courses each get very few
    examples since enrollments are split across every course
    individually.
  - `domain` is a small, bounded, semantically meaningful category
    already used elsewhere in this project (ml/encoding.py treats it
    as a nominal course field). Enrollments pool together across every
    course that shares a domain, giving the model far more signal per
    class, and a brand-new course becomes recommendable the instant
    it's tagged with a domain -- no retraining required.
  - This naturally splits the recommender into two stages: this model
    predicts the best-fit DOMAIN for a student; picking a specific
    course within that domain (e.g. matched to their semester/CGPA for
    an appropriate difficulty) is a simple filter, not an ML problem,
    and belongs in the FastAPI service layer, not here.

======================================================================
FEATURES (X): only fields a student provides on a fresh request.
======================================================================
degree, branch, learning_style, career_goal  -> nominal, LabelEncoder
interests                                     -> multi-label, MultiLabelBinarizer
cgpa, semester                                -> numeric, StandardScaler

Enrollment outcome fields (progress, quiz_score, status) are NEVER
features -- they don't exist yet at recommendation time. They're only
used upstream, in data_loader.build_training_dataset(), to decide which
past enrollments count as a "successful" match worth learning from.

======================================================================
ALGORITHM: Random Forest (compared against Logistic Regression as a
baseline; see the module docstring discussion in the chat for KNN/
Decision Tree reasoning).
======================================================================

======================================================================
COMPATIBILITY WITH encoders.joblib
======================================================================
This script is the thing that actually PRODUCES ml/artifacts/encoders.joblib,
by calling your existing ml/encoding.py functions (fit_encoders,
fit_multilabel_encoders) unchanged -- no logic in encoding.py is
modified. Encoders are fit once here, on the same student/course data
used for training, and saved. The FastAPI prediction endpoint must load
that same encoders.joblib (via ml.encoding.load_encoders) rather than
fitting its own -- see the "how this is used at inference time" note at
the bottom of this file.
"""

import os
import sys
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Reusing your existing encoding.py exactly as-is.
from ml.encoding import (
    fit_encoders, encode_dataframe,
    fit_multilabel_encoders, encode_multilabel_dataframe,
    save_encoders, ENCODERS_PATH,
    STUDENT_NOMINAL_COLUMNS, STUDENT_MULTI_LABEL_COLUMNS,
    COURSE_NOMINAL_COLUMNS, ORDINAL_COLUMN_ORDERS,
)
# Note: ml.data_loader (and app.database) are imported lazily inside
# run_from_db() below, not at module level -- train_and_evaluate() itself
# has no database dependency, so this file can be imported/tested without
# SQLAlchemy or a live DB connection.

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")

MODEL_PATH = os.path.join(ARTIFACT_DIR, "model.pkl")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "numeric_scaler.pkl")
REPORT_PATH = os.path.join(REPORT_DIR, "model_evaluation_report.json")

TARGET_COL = "domain"
NUMERIC_FEATURES = ["cgpa", "semester"]


def prepare_features(df: pd.DataFrame, encoders: dict, scaler: StandardScaler = None, fit_scaler: bool = False):
    """Turns a raw student-profile DataFrame into the numeric feature
    matrix X the model trains/predicts on, using the SAME encoders
    object for both training and inference so the two are always
    consistent with each other.

    Column order is built explicitly (nominal-encoded, then
    interests-encoded, then numeric) rather than inferred from
    `df.columns` -- this matters because a FastAPI request built from a
    dict/Pydantic model has no guaranteed field order, and sklearn
    validates that prediction-time column order matches training-time
    order exactly. Relying on incidental DataFrame column order was a
    real bug caught while testing this file; this is the fix.

    Set fit_scaler=True only during training (fits a new StandardScaler
    on this data); pass fit_scaler=False with an already-fitted scaler
    at inference time.
    """
    df = df.copy()

    # nominal fields -> LabelEncoder (degree, branch, learning_style, career_goal)
    df = encode_dataframe(df, encoders, columns=STUDENT_NOMINAL_COLUMNS, keep_original=False)
    nominal_feature_cols = [f"{c}_encoded" for c in STUDENT_NOMINAL_COLUMNS]

    # interests -> MultiLabelBinarizer (one 0/1 column per known interest)
    df = encode_multilabel_dataframe(df, encoders, columns=STUDENT_MULTI_LABEL_COLUMNS, keep_original=False)
    multilabel_feature_cols = [f"interests_{cls}" for cls in encoders["interests"].classes_]

    # numeric fields -> scaled, always in the same fixed order
    if fit_scaler:
        scaler = StandardScaler()
        df[NUMERIC_FEATURES] = scaler.fit_transform(df[NUMERIC_FEATURES])
    else:
        df[NUMERIC_FEATURES] = scaler.transform(df[NUMERIC_FEATURES])

    # Fixed, explicit column order -- independent of whatever order the
    # input DataFrame's columns happened to be in.
    feature_cols = nominal_feature_cols + multilabel_feature_cols + NUMERIC_FEATURES
    return df[feature_cols], scaler, feature_cols


def train_and_evaluate(training_df: pd.DataFrame, encoders: dict) -> dict:
    """training_df: output of data_loader.build_training_dataset(db).
    encoders: output of ml.encoding.fit_encoders / fit_multilabel_encoders
    (already fit on this same data by run_from_db(), below)."""

    if training_df[TARGET_COL].nunique() < 2:
        raise ValueError(
            f"Need at least 2 distinct course domains with completed enrollments to "
            f"train a classifier; found {training_df[TARGET_COL].nunique()}. "
            f"Add more completed-enrollment history first."
        )

    X, scaler, feature_cols = prepare_features(training_df, encoders, fit_scaler=True)

    # Target uses the SAME LabelEncoder that encoding.py already fit on
    # Course.domain -- not a separately-fit encoder -- so a predicted
    # class index decodes back to the exact same domain string used
    # everywhere else in the app (e.g. filtering Course.domain in SQL).
    domain_encoder = encoders["domain"]
    y = pd.Series(domain_encoder.transform(training_df[TARGET_COL].astype(str)))

    class_counts = y.value_counts()
    can_stratify = class_counts.min() >= 2
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if can_stratify else None,
    )

    candidates = {
        "RandomForest": RandomForestClassifier(
            n_estimators=300, min_samples_leaf=2, random_state=42, class_weight="balanced"
        ),
        "LogisticRegression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    }

    results = {}
    best_name, best_model, best_acc = None, None, -1
    min_class_count = int(class_counts.min())

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="macro")

        cv_mean, cv_std = None, None
        if min_class_count >= 2:
            cv_folds = min(5, min_class_count)
            if cv_folds >= 2:
                cv = cross_val_score(model, X, y, cv=cv_folds, scoring="accuracy")
                cv_mean, cv_std = float(cv.mean()), float(cv.std())

        results[name] = {
            "test_accuracy": round(float(acc), 4),
            "test_macro_f1": round(float(f1), 4),
            "cv_accuracy_mean": round(cv_mean, 4) if cv_mean is not None else None,
            "cv_accuracy_std": round(cv_std, 4) if cv_std is not None else None,
        }
        if acc > best_acc:
            best_name, best_model, best_acc = name, model, acc

    best_preds = best_model.predict(X_test)
    present_labels = sorted(set(y_test) | set(best_preds))
    class_report = classification_report(
        y_test, best_preds, labels=present_labels,
        target_names=domain_encoder.inverse_transform(present_labels),
        output_dict=True, zero_division=0,
    )
    cm = confusion_matrix(y_test, best_preds, labels=present_labels).tolist()

    feature_importance = {}
    if hasattr(best_model, "feature_importances_"):
        feature_importance = dict(
            sorted(zip(feature_cols, best_model.feature_importances_.tolist()), key=lambda kv: -kv[1])[:15]
        )

    report = {
        "target": TARGET_COL,
        "n_training_rows": len(training_df),
        "model_comparison": results,
        "best_model": best_name,
        "best_model_test_accuracy": round(float(best_acc), 4),
        "classification_report": class_report,
        "confusion_matrix": cm,
        "class_labels_in_test": list(domain_encoder.inverse_transform(present_labels)),
        "top_feature_importances": feature_importance,
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(results, indent=2))
    print(f"\nBest model: {best_name} (test accuracy = {best_acc:.4f})")
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved numeric scaler to {SCALER_PATH}")
    print(f"Saved evaluation report to {REPORT_PATH}")
    return report


def run_from_db():
    """Entry point for training against the real PostgreSQL database.

    1. Loads students/courses (needed to fit the encoders on the current
       vocabulary of degrees, branches, interests, career goals, and
       course domains).
    2. Fits and saves ml/artifacts/encoders.joblib via your existing
       encoding.py functions -- this IS how encoders.joblib gets
       (re)generated; run this script whenever you want to refresh both
       the encoders and the model together, so they never drift apart.
    3. Builds the labeled training dataset (completed enrollments only).
    4. Trains, evaluates, and saves model.pkl.
    """
    from app.database import SessionLocal
    from ml.data_loader import get_students_dataframe, get_courses_dataframe, build_training_dataset

    db = SessionLocal()
    try:
        students_df = get_students_dataframe(db)
        courses_df = get_courses_dataframe(db)

        # Fit encoders on the current student/course vocabulary and save
        # encoders.joblib -- reuses encoding.py's own functions unchanged.
        encoders = {}
        encoders.update(fit_encoders(students_df, nominal_columns=STUDENT_NOMINAL_COLUMNS))
        encoders.update(fit_multilabel_encoders(students_df, columns=STUDENT_MULTI_LABEL_COLUMNS))
        encoders.update(fit_encoders(courses_df, nominal_columns=COURSE_NOMINAL_COLUMNS,
                                       ordinal_columns=list(ORDINAL_COLUMN_ORDERS.keys())))
        save_encoders(encoders, ENCODERS_PATH)
        print(f"Fitted and saved encoders to {ENCODERS_PATH}")

        training_df = build_training_dataset(db)
        print(f"Built training dataset: {len(training_df)} completed-enrollment rows, "
              f"{training_df[TARGET_COL].nunique()} distinct domains")
    finally:
        db.close()

    if training_df.empty:
        raise ValueError(
            "No completed enrollments found -- nothing to train on yet. "
            "The model needs at least some historical completed enrollments "
            "before it has anything to learn from."
        )

    return train_and_evaluate(training_df, encoders)


if __name__ == "__main__":
    run_from_db()


# ======================================================================
# HOW model.pkl AND encoders.joblib ARE USED TOGETHER AT PREDICTION TIME
# ======================================================================
# In app/services/reccomendation.py (currently empty), a prediction
# endpoint would do roughly this:
#
#   from ml.encoding import load_encoders, encode_dataframe, encode_multilabel_dataframe, STUDENT_NOMINAL_COLUMNS, STUDENT_MULTI_LABEL_COLUMNS
#   import joblib, pandas as pd
#
#   encoders = load_encoders()                       # ml/artifacts/encoders.joblib
#   model = joblib.load("ml/artifacts/model.pkl")     # the trained classifier
#   scaler = joblib.load("ml/artifacts/numeric_scaler.pkl")
#
#   student_input = pd.DataFrame([{
#       "degree": "BTech", "branch": "CSE", "learning_style": "Visual",
#       "career_goal": "AI Engineer", "interests": "AI, Python",
#       "cgpa": 8.2, "semester": 4,
#   }])
#
#   X, _, _ = prepare_features(student_input, encoders, scaler=scaler, fit_scaler=False)
#   predicted_domain_code = model.predict(X)[0]
#   predicted_domain = encoders["domain"].inverse_transform([predicted_domain_code])[0]
#   confidence = model.predict_proba(X)[0].max()
#
#   # Stage 2 (no ML -- a simple filter): pick actual course(s) within
#   # that domain, e.g. matched to the student's level:
#   #   db.query(Course).filter(Course.domain == predicted_domain).all()
#
#   # Then persist it:
#   #   Recommendation(student_id=..., learning_path=predicted_domain, confidence=float(confidence))
#
# The critical constraint: encoders.joblib and model.pkl must always be
# regenerated TOGETHER (both come from run_from_db() in this file). If
# encoders.joblib is refit later without retraining the model, the
# integer codes it produces for degree/branch/career_goal/interests can
# shift, silently corrupting every prediction the old model makes.
