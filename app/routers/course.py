from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.course import (
    CourseCreate,
    CourseResponse
)

from app.services.course_service import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/", response_model=CourseResponse)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    return create_course(db, course)


@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return get_all_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = get_course_by_id(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.put("/{course_id}", response_model=CourseResponse)
def edit_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    updated = update_course(
        db,
        course_id,
        course
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return updated


@router.delete("/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_course(
        db,
        course_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully"
    }