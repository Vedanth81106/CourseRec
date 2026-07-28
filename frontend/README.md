# CourseRec Frontend

Next.js (App Router) + TypeScript + Tailwind frontend for the CourseRec backend.

## Setup

```bash
npm install
cp .env.local.example .env.local   # adjust NEXT_PUBLIC_API_BASE_URL if needed
npm run dev
```

The backend (FastAPI) must be running separately at whatever URL
`NEXT_PUBLIC_API_BASE_URL` points to (default `http://localhost:8000`).

## Structure

```
src/
  app/                          Routes (App Router). One folder per page.
    layout.tsx                  Root layout -- wraps the app in ActiveStudentProvider
    page.tsx                    Home page (placeholder for now)
    globals.css                 Tailwind base styles

  components/
    ui/                         Generic, reusable primitives (Button, Card).
                                 Not tied to any one page or backend resource.
    active-student-provider.tsx React context standing in for real auth
                                 (see note below)

  lib/
    api/
      client.ts                 Shared typed fetch wrapper (apiRequest<T>).
                                 Throws ApiError with the backend's own
                                 error message on failure.
      students.ts                One function per /students endpoint
      courses.ts                 One function per /courses endpoint
      enrollments.ts             One function per /enrollments endpoint
    active-student.ts           Plain localStorage read/write for the
                                 active-student stand-in
    utils.ts                    cn() -- Tailwind class merging helper

  types/
    api.ts                      TypeScript interfaces mirroring
                                 app/schemas/*.py exactly. Single source
                                 of truth for what the backend sends/expects.
```

## No real auth yet

`app/routers/auth.py` on the backend is currently an empty stub, so
there's no login endpoint to call. `ActiveStudentProvider` /
`useActiveStudent()` is a placeholder: it just remembers a chosen
`student_id` in `localStorage` so the rest of the app has a "current
student" concept to build against. When real auth exists on the
backend, only `active-student.ts` and `active-student-provider.tsx`
need to change -- every page using `useActiveStudent()` stays the same.

## No /predict integration yet

`app/routers/reccomendations.py` is also an empty stub on the backend.
Nothing in `lib/api/` calls it yet -- that gets added once the endpoint
exists.
