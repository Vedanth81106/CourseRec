from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    domain: str
    difficulty: str
    duration: int | None = None
    description: str | None = None 


class CourseResponse(BaseModel):
    course_id: int
    title: str
    domain: str
    difficulty: str
    duration: int | None = None
    description: str | None = None 

    class Config:
        from_attributes = True