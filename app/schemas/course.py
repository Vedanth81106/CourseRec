from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    domain: str
    difficulty: str
    duration: int
    description: str


class CourseResponse(BaseModel):
    course_id: int
    title: str
    domain: str
    difficulty: str
    duration: int
    description: str

    class Config:
        from_attributes = True