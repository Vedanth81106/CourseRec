import os

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.student import Student

from ml.encoding import load_encoders
from ml.train_model import prepare_features

ARTIFACT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "artifacts",
)

MODEL_PATH = os.path.join(ARTIFACT_DIR, "model.pkl")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "numeric_scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoders = load_encoders()


def recommend_courses(db: Session, student_id: int):
    student = (
        db.query(Student)
        .filter(Student.student_id == student_id)
        .first()
    )

    if student is None:
        return None

    student_df = pd.DataFrame([{
        "degree": student.degree,
        "branch": student.branch,
        "learning_style": student.learning_style,
        "career_goal": student.career_goal,
        "interests": student.interests,
        "cgpa": student.cgpa,
        "semester": student.semester,
    }])

    X, _, _ = prepare_features(
        student_df,
        encoders,
        scaler=scaler,
        fit_scaler=False,
    )

    predicted_code = model.predict(X)[0]

    predicted_domain = encoders["domain"].inverse_transform(
        [predicted_code]
    )[0]

    confidence = float(model.predict_proba(X).max())

    if student.semester <= 2:
        difficulty = "Beginner"
    elif student.semester <= 5:
        difficulty = "Intermediate"
    else:
        difficulty = "Advanced"

    courses = (
        db.query(Course)
        .filter(
            Course.domain == predicted_domain,
            Course.difficulty == difficulty
        )
        .order_by(Course.title)
        .limit(10)
        .all()
    )


    if len(courses) < 5:
        courses = (
            db.query(Course)
            .filter(Course.domain == predicted_domain)
            .order_by(Course.title)
            .limit(10)
            .all()
        )
    return {
        "student_id": student.student_id,
        "predicted_domain": predicted_domain,
        "recommended_difficulty": difficulty,
        "confidence": round(confidence,4),
        "courses": courses
    }