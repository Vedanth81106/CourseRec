from fastapi import FastAPI
from app.database import Base, engine
# import all the database models
from app.models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "CourseRec API is running"}