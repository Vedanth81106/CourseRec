import { apiRequest } from "./client";
import type { Course, CourseCreateInput, CourseUpdateInput } from "@/types/api";

// Mirrors app/routers/course.py exactly.

export function getCourses(): Promise<Course[]> {
  return apiRequest<Course[]>("/courses/");
}

export function getCourse(courseId: number): Promise<Course> {
  return apiRequest<Course>(`/courses/${courseId}`);
}

export function createCourse(input: CourseCreateInput): Promise<Course> {
  return apiRequest<Course>("/courses/", { method: "POST", body: input });
}

export function updateCourse(courseId: number, input: CourseUpdateInput): Promise<Course> {
  return apiRequest<Course>(`/courses/${courseId}`, { method: "PUT", body: input });
}

export function deleteCourse(courseId: number): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(`/courses/${courseId}`, { method: "DELETE" });
}
