from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate


def create_enrollment(db: Session, enrollment: EnrollmentCreate):

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        progress=enrollment.progress,
        quiz_score=enrollment.quiz_score,
        status=enrollment.status
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


def get_all_enrollments(db: Session):
    return db.query(Enrollment).all()


def get_enrollment_by_id(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(
        Enrollment.enrollment_id == enrollment_id
    ).first()


def update_enrollment(
    db: Session,
    enrollment_id: int,
    enrollment_data: EnrollmentCreate
):

    enrollment = db.query(Enrollment).filter(
        Enrollment.enrollment_id == enrollment_id
    ).first()

    if enrollment is None:
        return None

    enrollment.student_id = enrollment_data.student_id
    enrollment.course_id = enrollment_data.course_id
    enrollment.progress = enrollment_data.progress
    enrollment.quiz_score = enrollment_data.quiz_score
    enrollment.status = enrollment_data.status

    db.commit()
    db.refresh(enrollment)

    return enrollment


def delete_enrollment(db: Session, enrollment_id: int):

    enrollment = db.query(Enrollment).filter(
        Enrollment.enrollment_id == enrollment_id
    ).first()

    if enrollment is None:
        return None

    db.delete(enrollment)
    db.commit()

    return enrollment