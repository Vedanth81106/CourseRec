import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment

random.seed(42)

CAREER_TO_DOMAIN={
    "ML Engineer":"Data Science",
    "Data Scientist":"Data Science",
    "Backend Developer":"Web Development",
    "Cloud Engineer":"Cloud Computing",
    "Cyber Security":"Cyber Security",
}
KEYWORDS={
    "Python":["python","data","machine","ai"],
    "AI":["ai","machine","deep","generative"],
    "Machine Learning":["machine","learning","ai"],
    "Java":["java","spring"],
    "Spring":["spring","java"],
    "React":["react","web","javascript"],
    "JavaScript":["javascript","react","web"],
    "Linux":["linux","docker"],
    "Networking":["network","cloud"],
    "AWS":["aws","cloud"],
    "Docker":["docker","cloud"],
    "SQL":["sql","database","data"],
    "Data Science":["data","analytics"],
    "Cyber Security":["security","cyber","hack"],
    "Cloud":["cloud","aws","docker"],
}
def difficulty_for_semester(s):
    return ["Beginner"] if s<=2 else (["Beginner","Intermediate"] if s<=5 else ["Intermediate","Advanced"])
def score_from_cgpa(c):
    return random.randint(max(40,int(c*10-10)),min(100,int(c*10+5)))
def progress(status):
    return 100 if status=="Completed" else (0 if status=="Not Started" else random.randint(30,90))
def choose_status(diff):
    weights = {
        "Beginner": [75, 20, 5],
        "Intermediate": [45, 40, 15],
        "Advanced": [20, 50, 30],
    }

    return random.choices(
        ["Completed", "In Progress", "Not Started"],
        weights=weights.get(diff, [50, 35, 15]),
    )[0]
def seed_enrollments(db:Session):
    db.query(Enrollment).delete()
    db.commit()
    students=db.query(Student).all()
    courses=db.query(Course).all()
    for student in students:
        target=CAREER_TO_DOMAIN.get(student.career_goal)
        allowed=difficulty_for_semester(student.semester)
        interests=[i.strip() for i in (student.interests or "").split(",")]
        ranked=[]
        for course in courses:
            score=0
            if target and course.domain==target: score+=5
            if course.difficulty in allowed: score+=3
            text=f"{course.title} {course.description}".lower()
            for interest in interests:
                for kw in KEYWORDS.get(interest,[]):
                    if kw in text: score+=2
            score+=random.random()
            ranked.append((score,course))
        ranked.sort(key=lambda x:x[0],reverse=True)
        count=random.randint(max(2,student.semester),max(3,student.semester+3))
        for _,course in ranked[:count]:
            status=choose_status(course.difficulty)
            quiz=None if status=="Not Started" else score_from_cgpa(student.cgpa)
            db.add(Enrollment(student_id=student.student_id,course_id=course.course_id,status=status,progress=progress(status),quiz_score=quiz))
    db.commit()
    print("Done.")
def main():
    db=SessionLocal()
    try: seed_enrollments(db)
    finally: db.close()
if __name__=="__main__":
    main()
