// Typed client for the admin API (/api/admin/*).
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const TOKEN_KEY = "asp_admin_token";

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
  if (options.body) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* non-JSON */
    }
    const err = new Error(detail) as Error & { status?: number };
    err.status = res.status;
    throw err;
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// ---- Types ----
export interface User {
  id: string; email: string; name: string; is_admin: boolean;
  avatar_url?: string | null; bio?: string | null;
}
export interface AdminUser extends User {
  created_at: string; has_password: boolean;
}
export interface Stats {
  users: number; admins: number; phases: number; lessons: number;
  challenges: number; quiz_questions: number; submissions: number;
  passed_submissions: number; quiz_attempts: number;
}
export interface Phase {
  id: string; phase_number: number; title: string; description: string;
  estimated_hours: number; order: number; lesson_count: number;
}
export interface Lesson {
  id: string; phase_id: string; lesson_number: number; title: string;
  description: string; content_markdown: string; examples: unknown[];
  estimated_minutes: number; order: number;
}
export interface Challenge {
  id: string; lesson_id: string; title: string; description: string;
  starter_code: string; test_cases: unknown[]; difficulty: string;
  hints: unknown[]; solution_code: string; order: number;
}
export interface QuizQuestion {
  id: string; lesson_id: string; order: number; type: string; text: string;
  options: string[]; correct_answer: string; explanation: string;
}
export interface Submission {
  id: string; user_id: string; user_email: string; challenge_id: string;
  challenge_title: string; status: string; score: number; attempts: number;
  submitted_at: string;
}
export interface LessonListItem {
  id: string; phase_id: string; phase_number: number; phase_title: string;
  lesson_number: number; title: string; order: number;
}
export interface ChallengeListItem {
  id: string; lesson_id: string; lesson_title: string; title: string;
  difficulty: string; order: number;
}
export interface QuizListItem {
  id: string; lesson_id: string; lesson_title: string; type: string;
  text: string; order: number;
}

// ---- Endpoints ----
export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string; user: User }>("/api/auth/login", {
      method: "POST", body: JSON.stringify({ email, password }),
    }),
  me: () => request<User>("/api/auth/me"),

  stats: () => request<Stats>("/api/admin/stats"),

  users: (q?: string) =>
    request<AdminUser[]>(`/api/admin/users${q ? `?q=${encodeURIComponent(q)}` : ""}`),
  updateUser: (id: string, patch: Partial<Pick<AdminUser, "name" | "is_admin">>) =>
    request<AdminUser>(`/api/admin/users/${id}`, { method: "PATCH", body: JSON.stringify(patch) }),
  deleteUser: (id: string) =>
    request<void>(`/api/admin/users/${id}`, { method: "DELETE" }),

  submissions: (limit = 100) =>
    request<Submission[]>(`/api/admin/submissions?limit=${limit}`),

  phases: () => request<Phase[]>("/api/admin/phases"),
  createPhase: (body: Record<string, unknown>) =>
    request<Phase>("/api/admin/phases", { method: "POST", body: JSON.stringify(body) }),
  updatePhase: (id: string, body: Record<string, unknown>) =>
    request<Phase>(`/api/admin/phases/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  deletePhase: (id: string) =>
    request<void>(`/api/admin/phases/${id}`, { method: "DELETE" }),

  lessons: (phaseId: string) =>
    request<Lesson[]>(`/api/admin/phases/${phaseId}/lessons`),
  allLessons: (phaseId?: string) =>
    request<LessonListItem[]>(`/api/admin/lessons${phaseId ? `?phase_id=${phaseId}` : ""}`),
  lesson: (id: string) => request<Lesson>(`/api/admin/lessons/${id}`),
  createLesson: (body: Record<string, unknown>) =>
    request<Lesson>("/api/admin/lessons", { method: "POST", body: JSON.stringify(body) }),
  updateLesson: (id: string, body: Record<string, unknown>) =>
    request<Lesson>(`/api/admin/lessons/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  deleteLesson: (id: string) =>
    request<void>(`/api/admin/lessons/${id}`, { method: "DELETE" }),

  challenges: (lessonId: string) =>
    request<Challenge[]>(`/api/admin/lessons/${lessonId}/challenges`),
  allChallenges: (lessonId?: string) =>
    request<ChallengeListItem[]>(`/api/admin/challenges${lessonId ? `?lesson_id=${lessonId}` : ""}`),
  challenge: (id: string) => request<Challenge>(`/api/admin/challenges/${id}`),
  createChallenge: (body: Record<string, unknown>) =>
    request<Challenge>("/api/admin/challenges", { method: "POST", body: JSON.stringify(body) }),
  updateChallenge: (id: string, body: Record<string, unknown>) =>
    request<Challenge>(`/api/admin/challenges/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  deleteChallenge: (id: string) =>
    request<void>(`/api/admin/challenges/${id}`, { method: "DELETE" }),

  quiz: (lessonId: string) =>
    request<QuizQuestion[]>(`/api/admin/lessons/${lessonId}/quiz`),
  allQuiz: (lessonId?: string) =>
    request<QuizListItem[]>(`/api/admin/quiz${lessonId ? `?lesson_id=${lessonId}` : ""}`),
  quizQuestion: (id: string) => request<QuizQuestion>(`/api/admin/quiz/${id}`),
  createQuiz: (body: Record<string, unknown>) =>
    request<QuizQuestion>("/api/admin/quiz", { method: "POST", body: JSON.stringify(body) }),
  updateQuiz: (id: string, body: Record<string, unknown>) =>
    request<QuizQuestion>(`/api/admin/quiz/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  deleteQuiz: (id: string) =>
    request<void>(`/api/admin/quiz/${id}`, { method: "DELETE" }),
};
