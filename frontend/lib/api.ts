// Typed client for the FastAPI backend.

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Full-page redirect target to start an OAuth login with a provider. */
export function oauthLoginUrl(provider: string): string {
  return `${API_BASE}/api/auth/login/${provider}`;
}

const TOKEN_KEY = "asp_token";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null) {
  if (typeof window === "undefined") return;
  if (token) window.localStorage.setItem(TOKEN_KEY, token);
  else window.localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      /* non-JSON error body */
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// ---- Types (mirror the backend Pydantic schemas) ----
export interface User {
  id: string;
  email: string;
  name: string;
  avatar_url?: string | null;
  bio?: string | null;
}

export interface Phase {
  id: string;
  phase_number: number;
  title: string;
  description: string;
  estimated_hours: number;
  order: number;
}

export interface LessonSummary {
  id: string;
  lesson_number: number;
  title: string;
  description: string;
  estimated_minutes: number;
  order: number;
}

export interface PhaseDetail extends Phase {
  lessons: LessonSummary[];
}

export interface CodeExample {
  title: string;
  language: string;
  code: string;
}

export interface Challenge {
  id: string;
  lesson_id: string;
  title: string;
  description: string;
  starter_code: string;
  difficulty: string;
  hints: string[];
  order: number;
}

export interface Lesson {
  id: string;
  phase_id: string;
  lesson_number: number;
  title: string;
  description: string;
  content_markdown: string;
  examples: CodeExample[];
  estimated_minutes: number;
  order: number;
  challenges: Challenge[];
}

export interface TestResult {
  test_number: number;
  passed: boolean;
  expected?: string | null;
  actual?: string | null;
  error?: string | null;
}

export interface ExecuteResult {
  output: string;
  error?: string | null;
  test_results: TestResult[];
  all_tests_passed: boolean;
  execution_time: number;
  score: number;
}

export interface PhaseProgress {
  phase_id: string;
  phase_number: number;
  title: string;
  status: string;
  lessons_completed: number;
  total_lessons: number;
  challenges_solved: number;
  total_challenges: number;
  quizzes_passed: number;
  total_quizzes: number;
  progress_percentage: number;
}

export interface ProgressOverview {
  overall_percentage: number;
  challenges_solved: number;
  quizzes_passed: number;
  phases: PhaseProgress[];
}

// ---- Quizzes ----
export interface QuizQuestion {
  id: string;
  order: number;
  type: "multiple-choice" | "fill-blank";
  text: string;
  options: string[];
}

export interface Quiz {
  lesson_id: string;
  questions: QuizQuestion[];
}

export interface QuizQuestionResult {
  id: string;
  text: string;
  user_answer: string | null;
  correct_answer: string;
  correct: boolean;
  explanation: string;
}

export interface QuizResult {
  score: number;
  passed: boolean;
  correct_count: number;
  total: number;
  attempts: number;
  detailed_results: QuizQuestionResult[];
}

export interface OAuthProviders {
  github: boolean;
  google: boolean;
}

// ---- Endpoints ----
export const api = {
  devLogin: (email: string, name: string) =>
    request<{ access_token: string; user: User }>("/api/auth/dev-login", {
      method: "POST",
      body: JSON.stringify({ email, name }),
    }),
  register: (email: string, name: string, password: string) =>
    request<{ access_token: string; user: User }>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, name, password }),
    }),
  login: (email: string, password: string) =>
    request<{ access_token: string; user: User }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => request<User>("/api/auth/me"),
  phases: () => request<Phase[]>("/api/phases"),
  phase: (id: string) => request<PhaseDetail>(`/api/phases/${id}`),
  lesson: (id: string) => request<Lesson>(`/api/lessons/${id}`),
  executeCode: (challengeId: string, code: string) =>
    request<ExecuteResult>("/api/execute-code", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code }),
    }),
  progress: () => request<ProgressOverview>("/api/progress"),
  quiz: (lessonId: string) => request<Quiz>(`/api/lessons/${lessonId}/quiz`),
  submitQuiz: (lessonId: string, answers: Record<string, string>) =>
    request<QuizResult>(`/api/lessons/${lessonId}/quiz/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
  oauthProviders: () => request<OAuthProviders>("/api/auth/providers"),
};
