from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str
    degree: str
    branch: str
    semester: int
    cgpa: float
    interests: str
    learning_style: str
    career_goal: str 


class StudentResponse(BaseModel):
    student_id: int
    name: str
    email: str
    degree: str
    branch: str
    semester: int
    cgpa: float
    interests: str
    learning_style: str
    career_goal: str

class Config:
        from_attributes = True #not in pydantic form issok
        