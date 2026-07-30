from faker import Faker

from app.database import SessionLocal
from app.models.student import Student

fake = Faker()

DEGREES = ["B.Tech", "B.Sc", "BCA"]

BRANCHES = [
    "CSE",
    "IT",
    "ECE",
    "AI",
]

INTERESTS = [
    "Python, AI",
    "Java, Spring",
    "React, JavaScript",
    "Linux, Networking",
    "Cyber Security",
    "SQL, Data Science",
    "AWS, Docker",
]

LEARNING_STYLES = [
    "Video",
    "Reading",
    "Hands-on",
    "Visual",
]

CAREER_GOALS = [
    "ML Engineer",
    "Data Scientist",
    "Backend Developer",
    "Cloud Engineer",
    "Cyber Security",
]


def seed_students():
    db = SessionLocal()

    try:
        db.query(Student).delete()
        db.commit()

        students = []

        for _ in range(30):
            students.append(
                Student(
                    name=fake.name(),
                    email=fake.unique.email(),
                    degree=fake.random_element(DEGREES),
                    branch=fake.random_element(BRANCHES),
                    semester=fake.random_int(min=1, max=8),
                    cgpa=round(fake.pyfloat(min_value=6, max_value=10, right_digits=1), 1),
                    interests=fake.random_element(INTERESTS),
                    learning_style=fake.random_element(LEARNING_STYLES),
                    career_goal=fake.random_element(CAREER_GOALS),
                )
            )

        db.add_all(students)
        db.commit()

        print(f"Inserted {len(students)} students.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_students()