from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate


def create_course(db: Session, course: CourseCreate):

    new_course = Course(
        title=course.title,
        domain=course.domain,
        difficulty=course.difficulty,
        duration=course.duration,
        description=course.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_all_courses(db: Session):
    return db.query(Course).all()


def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(
        Course.course_id == course_id
    ).first()


def update_course(
    db: Session,
    course_id: int,
    course_data: CourseCreate
):

    course = db.query(Course).filter(
        Course.course_id == course_id
    ).first()

    if course is None:
        return None

    course.title = course_data.title
    course.domain = course_data.domain
    course.difficulty = course_data.difficulty
    course.duration = course_data.duration
    course.description = course_data.description

    db.commit()
    db.refresh(course)

    return course


def delete_course(db: Session, course_id: int):

    course = db.query(Course).filter(
        Course.course_id == course_id
    ).first()

    if course is None:
        return None

    db.delete(course)
    db.commit()

    return course