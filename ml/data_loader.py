"""
data_loader.py
---------------
Loads data from the PostgreSQL database (via the existing SQLAlchemy
models in app/models) into Pandas DataFrames, and assembles the
supervised training dataset used by train_model.py.

Two separate things live here:

1. Plain table loaders (get_students_dataframe, get_courses_dataframe,
   get_enrollments_dataframe) -- straightforward "give me this table as
   a DataFrame" helpers, reusing your existing models unchanged.

2. build_training_dataset() -- the actual ML dataset. One row per
   SUCCESSFUL past enrollment: the student's profile at the time
   (features) joined with the domain of the course they completed
   (label). Enrollment outcome fields (progress, quiz_score, status)
   are used ONLY to decide which enrollments count as "successful" --
   they are deliberately dropped before the row is handed to the
   model, because a fresh recommendation request has no progress/score
   yet. See the design note in train_model.py for why the target is
   course domain rather than course_id/course_name.
"""

import pandas as pd
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment

STUDENT_COLUMNS = [
    "student_id", "degree", "branch", "semester", "cgpa",
    "interests", "learning_style", "career_goal",
]
COURSE_COLUMNS = ["course_id", "title", "domain", "difficulty", "duration"]
ENROLLMENT_COLUMNS = ["enrollment_id", "student_id", "course_id", "progress", "quiz_score", "status"]

# What counts as a "successful" enrollment, i.e. a positive training example
# of "this course domain suited this student". Adjust if your app uses
# different status strings (e.g. "Completed" vs "completed" is handled by
# the case-insensitive compare below, but a totally different vocabulary
# like "finished" would need adding here).
SUCCESS_STATUSES = {"completed"}


def get_students_dataframe(db: Session) -> pd.DataFrame:
    """All students, as a DataFrame with one row per student."""
    rows = [{c: getattr(s, c) for c in STUDENT_COLUMNS} for s in db.query(Student).all()]
    return pd.DataFrame(rows, columns=STUDENT_COLUMNS)


def get_courses_dataframe(db: Session) -> pd.DataFrame:
    """All courses, as a DataFrame with one row per course."""
    rows = [{c: getattr(x, c) for c in COURSE_COLUMNS} for x in db.query(Course).all()]
    return pd.DataFrame(rows, columns=COURSE_COLUMNS)


def get_enrollments_dataframe(db: Session) -> pd.DataFrame:
    """All enrollments, as a DataFrame with one row per enrollment record."""
    rows = [{c: getattr(e, c) for c in ENROLLMENT_COLUMNS} for e in db.query(Enrollment).all()]
    return pd.DataFrame(rows, columns=ENROLLMENT_COLUMNS)


def build_training_dataset(db: Session, success_statuses=SUCCESS_STATUSES) -> pd.DataFrame:
    """Builds the supervised dataset for train_model.py.

    Returns one row per successfully-completed enrollment, containing:
        - the student's profile fields (the model's input features)
        - `domain`: the domain of the course they completed (the label)

    Enrollment outcome columns (progress, quiz_score, status) are used
    only as the filter that defines "successful" and are NOT included
    in the returned columns -- they must never leak into the feature
    set, since they don't exist yet for a brand-new recommendation
    request.
    """
    students_df = get_students_dataframe(db)
    courses_df = get_courses_dataframe(db)
    enrollments_df = get_enrollments_dataframe(db)

    if enrollments_df.empty or students_df.empty or courses_df.empty:
        return pd.DataFrame(columns=STUDENT_COLUMNS + ["domain"])

    successful = enrollments_df[
        enrollments_df["status"].astype(str).str.lower().isin(success_statuses)
    ]

    # join to get the domain of each completed course, and the profile of
    # the student who completed it
    merged = successful.merge(courses_df[["course_id", "domain"]], on="course_id", how="left")
    merged = merged.merge(students_df, on="student_id", how="left")

    training_df = merged[STUDENT_COLUMNS + ["domain"]].dropna(subset=["domain"])
    return training_df.reset_index(drop=True)
