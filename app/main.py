from app.routers.students import router as student_router
from app.routers.course import router as course_router
from fastapi import FastAPI
from app.database import Base, engine
# import all the database models
from app.models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)
app.include_router(course_router)

@app.get("/")
def home():
    return {"message": "CourseRec API is running"}