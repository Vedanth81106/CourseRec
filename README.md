# Course Recommendation System

## Prerequisites

Make sure you have the following installed:

- Git
- Docker
- Docker Compose

---

## 1. Clone the Repository

```bash
git clone https://github.com/Vedanth81106/CourseRec.git
cd CourseRec
```

---

## 2. Create the Environment File

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/courserec
```

> If you're using Docker Compose, `db` is the PostgreSQL service name.

---

## 3. Build and Start the Project

From the project root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL
- FastAPI Backend
- React Frontend

---

## 4. Access the Application

Frontend:

```
http://localhost:5173
```

Backend API:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

---

## 5. Import Courses

If the database is empty, import the Coursera dataset:

```bash
docker exec -it courserec-api python scripts/import_courses.py
```

---

## 6. Generate Sample Enrollments

```bash
docker exec -it courserec-api python scripts/enrollment_script.py
```

---

## 7. Train the ML Model

```bash
docker exec -it courserec-api python -m ml.train_model
```

This creates:

- `ml/artifacts/model.pkl`
- `ml/artifacts/encoders.joblib`
- `ml/artifacts/numeric_scaler.pkl`

---

## 8. Test the API

Open Swagger UI:

```
http://localhost:8000/docs
```

Example endpoints:

- `/students`
- `/courses`
- `/enrollments`
- `/recommend/{student_id}`

---

# Running Without Docker (Optional)

## 1. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux/macOS

```bash
python3 -m venv venv
```

---

## 2. Activate the Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create PostgreSQL Database

```sql
CREATE DATABASE courserec;
```

---

## 5. Create `.env`

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/courserec
```

---

## 6. Run the Backend

```bash
uvicorn app.main:app --reload
```

---

## 7. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Project Structure

```
CourseRec
├── app/                 # FastAPI backend
├── frontend/            # React + Vite frontend
├── ml/                  # ML training and inference
├── scripts/             # Data import and seeding scripts
├── data/                # CSV datasets
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```