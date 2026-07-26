from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse
)

from app.services.enrollment_service import (
    create_enrollment,
    get_all_enrollments,
    get_enrollment_by_id,
    update_enrollment,
    delete_enrollment
)

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router.post("/", response_model=EnrollmentResponse)
def add_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    return create_enrollment(db, enrollment)


@router.get("/", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    return get_all_enrollments(db)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):

    enrollment = get_enrollment_by_id(db, enrollment_id)

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def edit_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    updated = update_enrollment(
        db,
        enrollment_id,
        enrollment
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return updated


@router.delete("/{enrollment_id}")
def remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_enrollment(
        db,
        enrollment_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return {
        "message": "Enrollment deleted successfully"
    }