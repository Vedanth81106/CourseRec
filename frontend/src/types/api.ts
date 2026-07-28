/**
 * These mirror app/schemas/*.py exactly. If a backend schema changes,
 * update the matching type here first -- everything else in the
 * frontend (API functions, components, forms) should get a TypeScript
 * error pointing at what needs to change, rather than failing silently
 * at runtime.
 */

// ---- Students (app/schemas/student.py) ----

export interface Student {
  student_id: number;
  name: string;
  email: string;
  degree: string;
  branch: string;
  semester: number;
  cgpa: number;
  interests: string; // comma-separated, e.g. "AI, Python, Machine Learning"
  learning_style: string;
  career_goal: string;
}

// StudentCreate on the backend also requires email + password, even
// though those aren't part of what's shown back in StudentResponse.
export interface StudentCreateInput {
  name: string;
  email: string;
  password: string;
  degree: string;
  branch: string;
  semester: number;
  cgpa: number;
  interests: string;
  learning_style: string;
  career_goal: string;
}

// PUT /students/{id} reuses StudentCreate on the backend, so an update
// requires the same full payload (no partial updates yet).
export type StudentUpdateInput = StudentCreateInput;

// ---- Courses (app/schemas/course.py) ----

export interface Course {
  course_id: number;
  title: string;
  domain: string;
  difficulty: string;
  duration: number;
  description: string;
}

export interface CourseCreateInput {
  title: string;
  domain: string;
  difficulty: string;
  duration: number;
  description: string;
}

export type CourseUpdateInput = CourseCreateInput;

// ---- Enrollments (app/schemas/enrollment.py) ----

export interface Enrollment {
  enrollment_id: number;
  student_id: number;
  course_id: number;
  progress: number;
  quiz_score: number;
  status: string;
}

export interface EnrollmentCreateInput {
  student_id: number;
  course_id: number;
  progress: number;
  quiz_score: number;
  status: string;
}

export type EnrollmentUpdateInput = EnrollmentCreateInput;
