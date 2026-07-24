from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    domain = Column(String)
    difficulty = Column(String)
    duration = Column(Integer)
    description = Column(Text)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )