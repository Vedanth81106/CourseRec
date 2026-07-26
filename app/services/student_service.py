from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        name=student.name,
        email=student.email,
        password=student.password,
        degree=student.degree,
        branch=student.branch,
        semester=student.semester,
        cgpa=student.cgpa,
        interests=student.interests,
        learning_style=student.learning_style,
        career_goal=student.career_goal
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_all_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    return (
        db.query(Student)
        .filter(Student.student_id == student_id)
        .first()
    )

def update_student(db: Session, student_id: int, student_data: StudentCreate):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if student is None:
        return None

    student.name = student_data.name
    student.email = student_data.email
    student.password = student_data.password
    student.degree = student_data.degree
    student.branch = student_data.branch
    student.semester = student_data.semester
    student.cgpa = student_data.cgpa
    student.interests = student_data.interests
    student.learning_style = student_data.learning_style
    student.career_goal = student_data.career_goal

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student