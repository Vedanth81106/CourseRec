import { apiRequest } from "./client";
import type { Student, StudentCreateInput, StudentUpdateInput } from "@/types/api";

// Mirrors app/routers/students.py exactly.

export function getStudents(): Promise<Student[]> {
  return apiRequest<Student[]>("/students/");
}

export function getStudent(studentId: number): Promise<Student> {
  return apiRequest<Student>(`/students/${studentId}`);
}

export function createStudent(input: StudentCreateInput): Promise<Student> {
  return apiRequest<Student>("/students/", { method: "POST", body: input });
}

export function updateStudent(
  studentId: number,
  input: StudentUpdateInput
): Promise<Student> {
  return apiRequest<Student>(`/students/${studentId}`, { method: "PUT", body: input });
}

export function deleteStudent(studentId: number): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(`/students/${studentId}`, { method: "DELETE" });
}
