import type { Metadata } from "next";
import { ActiveStudentProvider } from "@/components/active-student-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "CourseRec",
  description: "Personalized course recommendations",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ActiveStudentProvider>{children}</ActiveStudentProvider>
      </body>
    </html>
  );
}
