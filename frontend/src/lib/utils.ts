import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines conditional classNames (clsx) and resolves Tailwind class
 * conflicts (tailwind-merge) so a component's default classes and a
 * caller's override classes (e.g. <Button className="w-full" />)
 * compose correctly instead of both applying and fighting each other.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
