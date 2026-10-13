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
# Interest keyword mappings
# --------------------------------------------------

INTEREST_KEYWORDS = {
    # Programming
    "python": ["python", "programming"],
    "machine learning": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
    ],
    "ai": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai",
    ],
    "java": ["java", "spring boot"],
    "javascript": ["javascript", "web development"],
    "react": ["react", "frontend", "front-end"],
    "html": ["html", "web development"],
    "css": ["css", "web design", "frontend"],

    # IoT and embedded systems
    "iot": [
        "internet of things",
        "iot",
        "sensors",
        "microcontrollers",
    ],
    "embedded systems": [
        "embedded systems",
        "microcontrollers",
        "firmware",
        "arduino",
        "esp32",
    ],

    # Electronics and electrical engineering
    "electronics": [
        "electronics",
        "circuits",
        "digital systems",
        "transistors",
    ],
    "digital electronics": [
        "digital electronics",
        "digital systems",
        "logic gates",
        "logic circuits",
    ],
    "digital electronics system design": [
        "digital systems",
        "digital electronics",
        "logic gates",
        "logic circuits",
    ],
    "communication systems": [
        "communication systems",
        "digital communications",
        "communication signals",
    ],
    "network analysis": [
        "network analysis",
        "circuit analysis",
        "linear circuits",
        "electrical networks",
    ],
    "signal processing": [
        "signal processing",
        "digital signal processing",
        "dsp",
        "signals",
    ],
    "electrical circuits": [
        "electrical circuits",
        "linear circuits",
        "circuit analysis",
        "electrical networks",
    ],
    "power systems": [
        "power systems",
        "electric power",
        "power generation",
        "power distribution",
    ],
    "power electronics": [
        "power electronics",
        "power converters",
        "dc-dc converters",
    ],
    "eee": [
        "electrical and electronics engineering",
        "electrical engineering",
        "electrical circuits",
        "power systems",
        "power electronics",
    ],
    "ece": [
        "electronics and communication engineering",
        "electronics",
        "communication systems",
        "signal processing",
        "digital systems",
    ],

    # Mechanical engineering
    "cad": [
        "computer aided design",
        "cad",
        "mechanical design",
    ],
    "robotics": [
        "robotics",
        "industrial robots",
        "robot automation",
    ],
    "manufacturing": [
        "manufacturing",
        "digital manufacturing",
        "production processes",
    ],
    "hydraulics": [
        "hydraulics",
        "fluid systems",
        "fluid power",
    ],
    "fluid mechanics": [
        "fluid mechanics",
        "fluid systems",
        "fluid dynamics",
    ],
    "machine design": [
        "machine design",
        "mechanical design",
        "machine elements",
    ],
    "design of machine elements": [
        "machine design",
        "mechanical design",
        "machine elements",
    ],
    "mechanical engineering": [
        "mechanical engineering",
        "thermodynamics",
        "machine design",
        "engineering mechanics",
    ],

    # Cloud computing
    "cloud": [
        "cloud computing",
        "cloud infrastructure",
        "aws",
        "azure",
    ],
    "aws": [
        "aws",
        "amazon web services",
        "cloud computing",
    ],
    "azure": [
        "azure",
        "microsoft azure",
        "cloud infrastructure",
    ],
    "cloud infrastructure": [
        "cloud infrastructure",
        "virtual machines",
        "cloud computing",
        "azure",
        "aws",
    ],

    # Other areas
    "networking": [
        "networking",
        "computer networks",
        "network security",
        "tcp/ip",
    ],
    "cyber security": [
        "cybersecurity",
        "cyber security",
        "network security",
        "ethical hacking",
    ],
    "linux": ["linux", "operating systems"],
    "sql": ["sql", "database", "postgresql"],
    "data science": ["data science", "data analytics"],
}


# --------------------------------------------------
# Career goal keyword mappings
# --------------------------------------------------

CAREER_KEYWORDS = {
    "ml engineer": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
    ],
    "data scientist": [
        "data science",
        "statistics",
        "data analytics",
    ],
    "web developer": [
        "web development",
        "javascript",
        "html",
        "css",
    ],
    "backend developer": [
        "backend",
        "api",
        "database",
        "server-side",
    ],
    "cloud engineer": [
        "cloud computing",
        "cloud infrastructure",
        "aws",
        "azure",
    ],
    "cyber security": [
        "cyber security",
        "cybersecurity",
        "ethical hacking",
    ],
    "iot engineer": [
        "internet of things",
        "iot",
        "sensors",
        "microcontrollers",
    ],
    "embedded systems engineer": [
        "embedded systems",
        "firmware",
        "microcontrollers",
    ],
    "eee engineer": [
        "electrical circuits",
        "power systems",
        "power electronics",
        "electrical engineering",
    ],
    "electrical engineer": [
        "electrical circuits",
        "power systems",
        "power electronics",
        "electrical engineering",
    ],
    "ece engineer": [
        "electronics",
        "communication systems",
        "signal processing",
        "digital systems",
    ],
    "electronics engineer": [
        "electronics",
        "communication systems",
        "digital systems",
    ],
    "mechanical engineer": [
        "mechanical engineering",
        "cad",
        "robotics",
        "manufacturing",
        "thermodynamics",
    ],
    "mechanical design engineer": [
        "machine design",
        "mechanical design",
        "cad",
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


def normalize_branch(value):
    """Normalize common branch abbreviations without case sensitivity."""
    branch = normalize_text(value).upper()
    aliases = {
        "CSE": "CSE", "CS": "CSE", "COMPUTER SCIENCE": "CSE",
        "ISE": "ISE", "IS": "ISE", "INFORMATION SCIENCE": "ISE",
        "ECE": "ECE", "EC": "ECE", "ELECTRONICS AND COMMUNICATION ENGINEERING": "ECE",
        "EEE": "EEE", "EE": "EEE", "ELECTRICAL AND ELECTRONICS ENGINEERING": "EEE",
        "ME": "ME", "MECH": "ME", "MECHANICAL": "ME", "MECHANICAL ENGINEERING": "ME",
        "AIML": "AIML", "AI ML": "AIML", "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING": "AIML",
        "AI": "AI", "ARTIFICIAL INTELLIGENCE": "AI",
        "CIVIL": "CIVIL", "CIVIL ENGINEERING": "CIVIL",
    }
    return aliases.get(branch, branch)


BRANCH_DOMAIN_LABELS = {
    "CSE": "Computer Science",
    "ISE": "Information Science",
    "ECE": "Electronics and Communication Engineering",
    "EEE": "Electrical and Electronics Engineering",
    "ME": "Mechanical Engineering",
    "AIML": "Artificial Intelligence and Machine Learning",
    "AI": "Artificial Intelligence",
    "CIVIL": "Civil Engineering",
}


BRANCH_COURSE_KEYWORDS = {
    "CSE": ["computer science", "programming", "software", "web development", "data science"],
    "ISE": ["information science", "programming", "software", "database", "web development"],
    "ECE": ["electronics", "communication systems", "signal processing", "dsp", "vlsi", "sensors", "embedded systems", "digital systems", "robotics"],
    "EEE": ["electrical", "electric motor", "motor control", "power systems", "power electronics", "circuits", "sensors"],
    "ME": ["mechanical", "robotics", "cad", "manufacturing", "machine design", "fluid mechanics", "automation"],
    "AIML": ["artificial intelligence", "machine learning", "deep learning", "data science"],
    "AI": ["artificial intelligence", "machine learning", "deep learning"],
    "CIVIL": ["civil engineering", "construction", "structural", "surveying"],
}


def calculate_relevance(course, interests, career_goal, branch=None):
    """
    Rank courses using branch, interests, career goals, titles,
    descriptions, and domains.
    """

    title = normalize_text(course.title)
    description = normalize_text(course.description)
    domain = normalize_text(course.domain)

    score = 0

    # Student interests receive the strongest influence.
    for interest in interests:
        keywords = INTEREST_KEYWORDS.get(
            interest,
            [interest],
        )

        for keyword in keywords:
            keyword = normalize_text(keyword)

            if keyword and keyword in title:
                score += 12
            elif keyword and keyword in description:
                score += 5
            elif keyword and keyword in domain:
                score += 4

    # Career goal also influences ranking strongly.
    career = normalize_text(career_goal)

    career_keywords = CAREER_KEYWORDS.get(
        career,
        [career] if career else [],
    )

    for keyword in career_keywords:
        keyword = normalize_text(keyword)

        if keyword and keyword in title:
            score += 8
        elif keyword and keyword in description:
            score += 4
        elif keyword and keyword in domain:
            score += 5

    # Exact engineering domain matches get an extra boost.
    engineering_domains = {
        "eee": [
            "electrical and electronics engineering (eee)",
            "electrical engineering",
        ],
        "electrical engineer": [
            "electrical and electronics engineering (eee)",
            "electrical engineering",
        ],
        "eee engineer": [
            "electrical and electronics engineering (eee)",
            "electrical engineering",
        ],
        "ece": [
            "electronics and communication engineering (ece)",
            "electronics and communication engineering",
        ],
        "ece engineer": [
            "electronics and communication engineering (ece)",
            "electronics and communication engineering",
        ],
        "mechanical engineer": [
            "mechanical engineering",
        ],
        "mechanical design engineer": [
            "mechanical engineering",
        ],
    }

    for career_key, matching_domains in engineering_domains.items():
        if career == career_key:
            if any(
                domain == normalize_text(matching_domain)
                or normalize_text(matching_domain) in domain
                for matching_domain in matching_domains
            ):
                score += 15

    # Branch is a strong relevance signal, but does not exclude other courses.
    normalized_branch = normalize_branch(branch) if branch else ""
    branch_keywords = BRANCH_COURSE_KEYWORDS.get(normalized_branch, [])
    combined_text = f"{title} {description} {domain}"
    if normalized_branch:
        canonical_label = normalize_text(BRANCH_DOMAIN_LABELS.get(normalized_branch, ""))
        if canonical_label and canonical_label in domain:
            score += 15
        for keyword in branch_keywords:
            if keyword in combined_text:
                score += 6
                break

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

    # Predict the broad domain.
    X, _, _ = prepare_features(
        student_df,
        encoders,
        scaler=scaler,
        fit_scaler=False,
    )

    predicted_code = model.predict(X)[0]

    # Keep the ML model's prediction as a separate diagnostic signal.
    ml_predicted_domain = encoders["domain"].inverse_transform(
        [predicted_code]
    )[0]

    # This is the model's confidence in its own prediction, not a confidence
    # score for the branch-based display override below.
    probabilities = model.predict_proba(X)[0]
    confidence = float(probabilities.max())

    # Prefer the student's stated branch for the displayed domain.
    # Matching is case-insensitive and supports common abbreviations.
    normalized_branch = normalize_branch(student.branch)
    predicted_domain = BRANCH_DOMAIN_LABELS.get(
        normalized_branch,
        ml_predicted_domain,
    )

    # Determine preferred difficulty.
    difficulty = get_difficulty(student.semester)

    # Get all courses.
    all_courses = db.query(Course).all()

    interests = get_student_interests(student)

    # Score each course.
    ranked_courses = []

    for course in all_courses:

        relevance_score = calculate_relevance(
            course,
            interests,
            student.career_goal,
            student.branch,
        )

        # Keep the ML model's original prediction as a small tie-breaker.
        if normalize_text(course.domain) == normalize_text(ml_predicted_domain):
            relevance_score += 1

        # Prefer suitable difficulty without excluding other levels.
        if normalize_text(course.difficulty) == normalize_text(
            difficulty
        ):
            relevance_score += 2

        ranked_courses.append(
            (relevance_score, course)
        )

    # Sort by relevance, then by title.
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
    print("Student branch:", student.branch)
    print("Displayed domain:", predicted_domain)
    print("ML-predicted domain:", ml_predicted_domain)
    print("ML confidence:", round(confidence, 4))
    print("Recommended difficulty:", difficulty)

    print(
        "Recommended courses:",
        [course.title for course in recommended_courses],
    )

    print("===========================================\n")

    return {
        "student_id": student.student_id,
        "predicted_domain": predicted_domain,
        "ml_predicted_domain": ml_predicted_domain,
        "recommended_difficulty": difficulty,
        "confidence": round(confidence, 4),
        "courses": recommended_courses,
    }