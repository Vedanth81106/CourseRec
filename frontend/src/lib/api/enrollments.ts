import { apiRequest } from "./client";
import type { Enrollment, EnrollmentCreateInput, EnrollmentUpdateInput } from "@/types/api";

// Mirrors app/routers/enrollment.py exactly.

export function getEnrollments(): Promise<Enrollment[]> {
  return apiRequest<Enrollment[]>("/enrollments/");
}

export function getEnrollment(enrollmentId: number): Promise<Enrollment> {
  return apiRequest<Enrollment>(`/enrollments/${enrollmentId}`);
}

export function createEnrollment(input: EnrollmentCreateInput): Promise<Enrollment> {
  return apiRequest<Enrollment>("/enrollments/", { method: "POST", body: input });
}

export function updateEnrollment(
  enrollmentId: number,
  input: EnrollmentUpdateInput
): Promise<Enrollment> {
  return apiRequest<Enrollment>(`/enrollments/${enrollmentId}`, { method: "PUT", body: input });
}

export function deleteEnrollment(enrollmentId: number): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(`/enrollments/${enrollmentId}`, { method: "DELETE" });
}
