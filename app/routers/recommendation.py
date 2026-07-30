from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.recommendation_service import recommend_courses

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{student_id}")
def get_recommendation(student_id: int, db: Session = Depends(get_db)):
    result = recommend_courses(db, student_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result