const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  cache?: RequestCache;
}

/**
 * Core request function every resource module (students.ts, courses.ts,
 * enrollments.ts) calls through. Handles:
 *   - building the full URL from NEXT_PUBLIC_API_BASE_URL
 *   - JSON encoding the request body
 *   - parsing the response, or throwing ApiError with the backend's own
 *     `detail` message (FastAPI's HTTPException shape) when the request fails
 *   - the 204/empty-body case (e.g. DELETE endpoints that return nothing)
 */
export async function apiRequest<TResponse>(
  path: string,
  options: RequestOptions = {}
): Promise<TResponse> {
  const { method = "GET", body, cache } = options;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    cache,
  });

  if (!response.ok) {
    let message = `Request to ${path} failed with status ${response.status}`;
    try {
      const errorBody = await response.json();
      if (typeof errorBody?.detail === "string") {
        message = errorBody.detail; // FastAPI's HTTPException(detail=...) shape
      }
    } catch {
      // response body wasn't JSON -- fall back to the generic message above
    }
    throw new ApiError(response.status, message);
  }

  if (response.status === 204) {
    return undefined as TResponse;
  }

  return response.json() as Promise<TResponse>;
}
