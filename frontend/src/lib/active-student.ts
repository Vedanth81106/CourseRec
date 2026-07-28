/**
 * Stand-in for real authentication, which doesn't exist on the backend
 * yet (app/routers/auth.py is an empty stub). Persists which student is
 * "logged in" as just an ID in localStorage. Every page that needs to
 * know the current student should go through the useActiveStudent()
 * hook in active-student-provider.tsx, not import this file directly --
 * this file only exists so that hook has somewhere to persist to.
 *
 * When real auth is built, this file and the provider are the only two
 * things that need to change; every page consuming useActiveStudent()
 * stays the same.
 */

const STORAGE_KEY = "courserec_active_student_id";

export function readActiveStudentId(): number | null {
  if (typeof window === "undefined") return null; // SSR guard
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
}

export function writeActiveStudentId(studentId: number): void {
  window.localStorage.setItem(STORAGE_KEY, String(studentId));
}

export function clearActiveStudentId(): void {
  window.localStorage.removeItem(STORAGE_KEY);
}
