from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class StudentSkill(Base):
    __tablename__ = "student_skills"

    skill_id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.student_id"),
        nullable=False
    )

    skill = Column(String, nullable=False)

    student = relationship("Student", back_populates="skills")