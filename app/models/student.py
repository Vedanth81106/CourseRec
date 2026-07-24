from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    degree = Column(String)
    branch = Column(String)
    semester = Column(Integer)

    cgpa = Column(Float)

    interests = Column(String)
    learning_style = Column(String)
    career_goal = Column(String)

    skills = relationship(
        "StudentSkill",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="student",
        cascade="all, delete-orphan"
    )