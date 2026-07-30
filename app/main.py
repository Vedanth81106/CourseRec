from app.routers.students import router as student_router
from app.routers.course import router as course_router
from app.routers.enrollment import router as enrollment_router
from app.routers.recommendation import router as recommendation_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import Base, engine
# import all the database models
from app.models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(recommendation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "CourseRec API is running"}