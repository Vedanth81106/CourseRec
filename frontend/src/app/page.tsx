import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

// Placeholder only -- this gets replaced when we build the real home
// page next. Its only job right now is to confirm the project structure
// (Tailwind, the Card primitive, the layout/provider) actually renders.
export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl items-center justify-center p-6">
      <Card>
        <CardHeader>
          <CardTitle>CourseRec</CardTitle>
          <CardDescription>Frontend scaffold is up and running.</CardDescription>
        </CardHeader>
      </Card>
    </main>
  );
}
