"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import {
  readActiveStudentId,
  writeActiveStudentId,
  clearActiveStudentId,
} from "@/lib/active-student";

interface ActiveStudentContextValue {
  studentId: number | null;
  /** true until the initial localStorage read completes, so pages can
   * avoid a flash of "no student selected" on first render */
  isLoaded: boolean;
  setStudentId: (id: number) => void;
  clearStudentId: () => void;
}

const ActiveStudentContext = createContext<ActiveStudentContextValue | null>(null);

export function ActiveStudentProvider({ children }: { children: ReactNode }) {
  const [studentId, setStudentIdState] = useState<number | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setStudentIdState(readActiveStudentId());
    setIsLoaded(true);
  }, []);

  const setStudentId = (id: number) => {
    writeActiveStudentId(id);
    setStudentIdState(id);
  };

  const clearStudentId = () => {
    clearActiveStudentId();
    setStudentIdState(null);
  };

  return (
    <ActiveStudentContext.Provider
      value={{ studentId, isLoaded, setStudentId, clearStudentId }}
    >
      {children}
    </ActiveStudentContext.Provider>
  );
}

/** The hook every page/component should use to read or change who the
 * "current student" is -- never read localStorage directly. */
export function useActiveStudent() {
  const ctx = useContext(ActiveStudentContext);
  if (!ctx) {
    throw new Error("useActiveStudent must be used within an ActiveStudentProvider");
  }
  return ctx;
}
