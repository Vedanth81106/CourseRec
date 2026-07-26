from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import *

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post("/", response_model=StudentResponse)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student(db, student)


@router.put("/{student_id}", response_model=StudentResponse)
def edit_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    updated = update_student(db, student_id, student)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated


@router.delete("/{student_id}")
def remove_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_student(db, student_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"message": "Student deleted successfully"}