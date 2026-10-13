import os

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.student import Student

from ml.encoding import load_encoders
from ml.train_model import prepare_features


# --------------------------------------------------
# Load ML artifacts
# --------------------------------------------------

ARTIFACT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "ml",
    "artifacts",
)

MODEL_PATH = os.path.join(ARTIFACT_DIR, "model.pkl")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "numeric_scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoders = load_encoders()


# --------------------------------------------------
# Interest and career keyword mappings
# --------------------------------------------------

INTEREST_KEYWORDS = {
    "python": ["python", "programming"],
    "machine learning": [
        "machine learning", "machine-learning",
        "ml", "artificial intelligence",
    ],
    "ai": [
        "artificial intelligence", "machine learning",
        "deep learning", "generative ai",
    ],
    "java": ["java", "spring boot"],
    "javascript": ["javascript", "js", "web development"],
    "react": ["react", "frontend", "front-end"],
    "html": ["html", "web development"],
    "css": ["css", "web design", "frontend"],
    "iot": [
        "internet of things", "iot", "embedded systems",
        "sensors", "microcontrollers",
    ],
    "embedded systems": [
        "embedded systems", "microcontrollers",
        "firmware", "arduino", "esp32",
    ],
    "electronics": [
        "electronics", "circuits", "microcontrollers",
        "embedded systems",
    ],
    "networking": [
        "networking", "computer networks",
        "network security", "tcp/ip",
    ],
    "cyber security": [
        "cybersecurity", "cyber security",
        "network security", "ethical hacking",
    ],
    "linux": ["linux", "operating systems"],
    "cloud": ["cloud computing", "aws", "azure"],
    "aws": ["aws", "amazon web services", "cloud computing"],
    "sql": ["sql", "database", "postgresql"],
    "data science": ["data science", "data analytics"],
}


CAREER_KEYWORDS = {
    "ml engineer": [
        "machine learning", "artificial intelligence",
        "deep learning", "data science",
    ],
    "data scientist": [
        "data science", "statistics", "data analytics",
        "machine learning",
    ],
    "web developer": [
        "web development", "javascript", "html",
        "css", "frontend", "backend",
    ],
    "backend developer": [
        "backend", "back-end", "api",
        "database", "server-side",
    ],
    "cloud engineer": [
        "cloud computing", "aws", "azure",
        "docker", "devops",
    ],
    "cyber security": [
        "cyber security", "cybersecurity",
        "ethical hacking", "network security",
    ],
    "iot engineer": [
        "internet of things", "iot",
        "embedded systems", "sensors",
        "microcontrollers", "arduino", "esp32",
    ],
    "embedded systems engineer": [
        "embedded systems", "firmware",
        "microcontrollers", "arduino", "esp32",
    ],
}


# --------------------------------------------------
# Text helpers
# --------------------------------------------------

def normalize_text(value):
    """Convert text to lowercase for matching."""
    return str(value or "").strip().lower()


def get_student_interests(student):
    """Convert comma-separated interests into a list."""
    return [
        interest.strip().lower()
        for interest in (student.interests or "").split(",")
        if interest.strip()
    ]


def get_difficulty(semester):
    """Choose the preferred course difficulty."""
    if semester <= 2:
        return "Beginner"
    elif semester <= 5:
        return "Intermediate"
    return "Advanced"


def calculate_relevance(course, interests, career_goal):
    """
    Rank a course using the student's interests,
    career goal, title, and description.
    """

    title = normalize_text(course.title)
    description = normalize_text(course.description)
    domain = normalize_text(course.domain)

    # Title matches receive more weight than description matches.
    score = 0

    for interest in interests:
        keywords = INTEREST_KEYWORDS.get(
            interest,
            [interest],
        )

        for keyword in keywords:
            keyword = keyword.lower()

            if keyword in title:
                score += 10
            elif keyword in description:
                score += 4
            elif keyword in domain:
                score += 3

    # Reward courses relevant to the career goal.
    career = normalize_text(career_goal)

    career_keywords = CAREER_KEYWORDS.get(
        career,
        [career] if career else [],
    )

    for keyword in career_keywords:
        if keyword in title:
            score += 6
        elif keyword in description:
            score += 3
        elif keyword in domain:
            score += 2

    return score


# --------------------------------------------------
# Course recommendation function
# --------------------------------------------------

def recommend_courses(db: Session, student_id: int):

    # Find the student.
    student = (
        db.query(Student)
        .filter(Student.student_id == student_id)
        .first()
    )

    if student is None:
        return None

    # Prepare student information for the ML model.
    student_df = pd.DataFrame([{
        "degree": student.degree,
        "branch": student.branch,
        "learning_style": student.learning_style,
        "career_goal": student.career_goal,
        "interests": student.interests,
        "cgpa": student.cgpa,
        "semester": student.semester,
    }])

    # Predict the most suitable domain.
    X, _, _ = prepare_features(
        student_df,
        encoders,
        scaler=scaler,
        fit_scaler=False,
    )

    predicted_code = model.predict(X)[0]

    predicted_domain = encoders["domain"].inverse_transform(
        [predicted_code]
    )[0]

    # Calculate model confidence.
    probabilities = model.predict_proba(X)[0]
    confidence = float(probabilities.max())

    # Determine preferred difficulty.
    difficulty = get_difficulty(student.semester)

    # Get all courses so interests can influence ranking.
    all_courses = db.query(Course).all()

    interests = get_student_interests(student)

    # Score each course individually.
    ranked_courses = []

    for course in all_courses:

        relevance_score = calculate_relevance(
            course,
            interests,
            student.career_goal,
        )

        # Give a smaller bonus to the predicted domain.
        if normalize_text(course.domain) == normalize_text(
            predicted_domain
        ):
            relevance_score += 2

        # Prefer suitable difficulty without excluding other levels.
        if normalize_text(course.difficulty) == normalize_text(
            difficulty
        ):
            relevance_score += 2

        ranked_courses.append(
            (relevance_score, course)
        )

    # Highest relevance first.
    ranked_courses.sort(
        key=lambda item: (
            item[0],
            normalize_text(item[1].title),
        ),
        reverse=True,
    )

    # Return the ten highest-ranked courses.
    recommended_courses = [
        course
        for score, course in ranked_courses[:10]
    ]

    # Diagnostic logs.
    print("\n========== COURSE RECOMMENDATION ==========")
    print("Student ID:", student.student_id)
    print("Interests:", student.interests)
    print("Career goal:", student.career_goal)
    print("Predicted domain:", predicted_domain)
    print("Confidence:", round(confidence, 4))
    print("Recommended difficulty:", difficulty)

    print(
        "Recommended courses:",
        [course.title for course in recommended_courses],
    )

    print("===========================================\n")

    return {
        "student_id": student.student_id,
        "predicted_domain": predicted_domain,
        "recommended_difficulty": difficulty,
        "confidence": round(confidence, 4),
        "courses": recommended_courses,
    }