from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import create_student

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/")
def get_students():
    return {"message": "Student route works"}


@router.post("/", response_model=StudentResponse)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student(db, student)