from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    progress: int
    quiz_score: float
    status: str


class EnrollmentResponse(BaseModel):
    enrollment_id: int
    student_id: int
    course_id: int
    progress: int
    quiz_score: float
    status: str

    class Config:
        from_attributes = True