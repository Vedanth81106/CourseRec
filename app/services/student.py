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