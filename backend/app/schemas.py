"""Pydantic request/response models for the API."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---- Auth ----
class DevLoginRequest(BaseModel):
    email: EmailStr = "demo@studyplatform.dev"
    name: str = "Demo Learner"


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(ORMModel):
    id: str
    email: str
    name: str
    avatar_url: str | None = None
    bio: str | None = None
    is_admin: bool = False


# ---- Content ----
class ChallengeOut(ORMModel):
    id: str
    lesson_id: str
    title: str
    description: str
    starter_code: str
    difficulty: str
    hints: list
    order: int
    # NOTE: test_cases and solution_code are intentionally omitted from the
    # public payload so answers aren't shipped to the browser.


class LessonOut(ORMModel):
    id: str
    phase_id: str
    lesson_number: int
    title: str
    description: str
    content_markdown: str
    examples: list
    estimated_minutes: int
    order: int
    challenges: list[ChallengeOut] = []


class LessonSummary(ORMModel):
    id: str
    lesson_number: int
    title: str
    description: str
    estimated_minutes: int
    order: int


class PhaseOut(ORMModel):
    id: str
    phase_number: int
    title: str
    description: str
    estimated_hours: int
    order: int


class PhaseDetail(PhaseOut):
    lessons: list[LessonSummary] = []


# ---- Code execution ----
class ExecuteCodeRequest(BaseModel):
    code: str
    challenge_id: str


class TestResult(BaseModel):
    test_number: int
    passed: bool
    expected: str | None = None
    actual: str | None = None
    error: str | None = None


class ExecuteCodeResponse(BaseModel):
    output: str = ""
    error: str | None = None
    test_results: list[TestResult] = []
    all_tests_passed: bool = False
    execution_time: float = 0.0
    score: int = 0


# ---- Quizzes ----
class QuizQuestionOut(ORMModel):
    id: str
    order: int
    type: str
    text: str
    options: list
    # correct_answer and explanation are intentionally omitted from the public
    # payload so answers aren't shipped to the browser before submission.


class QuizOut(BaseModel):
    lesson_id: str
    questions: list[QuizQuestionOut]


class QuizSubmission(BaseModel):
    # question_id -> the user's answer
    answers: dict[str, str]


class QuizQuestionResult(BaseModel):
    id: str
    text: str
    user_answer: str | None
    correct_answer: str
    correct: bool
    explanation: str


class QuizResult(BaseModel):
    score: int  # 0-100
    passed: bool  # score >= 80
    correct_count: int
    total: int
    attempts: int
    detailed_results: list[QuizQuestionResult]


# ---- Progress ----
class PhaseProgress(BaseModel):
    phase_id: str
    phase_number: int
    title: str
    status: str
    lessons_completed: int
    total_lessons: int
    challenges_solved: int
    total_challenges: int
    quizzes_passed: int
    total_quizzes: int
    progress_percentage: float


class ProgressOverview(BaseModel):
    overall_percentage: float
    challenges_solved: int
    quizzes_passed: int
    phases: list[PhaseProgress]


# ---- Admin ----
class AdminStats(BaseModel):
    users: int
    admins: int
    phases: int
    lessons: int
    challenges: int
    quiz_questions: int
    submissions: int
    passed_submissions: int
    quiz_attempts: int


class AdminUserOut(ORMModel):
    id: str
    email: str
    name: str
    is_admin: bool
    avatar_url: str | None = None
    created_at: datetime
    has_password: bool = False


class UserUpdate(BaseModel):
    name: str | None = None
    is_admin: bool | None = None


class PhaseIn(BaseModel):
    phase_number: int
    title: str
    description: str = ""
    estimated_hours: int = 0
    order: int = 0


class PhaseUpdate(BaseModel):
    phase_number: int | None = None
    title: str | None = None
    description: str | None = None
    estimated_hours: int | None = None
    order: int | None = None


class AdminPhaseOut(ORMModel):
    id: str
    phase_number: int
    title: str
    description: str
    estimated_hours: int
    order: int
    lesson_count: int = 0


class LessonIn(BaseModel):
    phase_id: str
    lesson_number: int
    title: str
    description: str = ""
    content_markdown: str = ""
    examples: list = []
    estimated_minutes: int = 0
    order: int = 0


class LessonUpdate(BaseModel):
    lesson_number: int | None = None
    title: str | None = None
    description: str | None = None
    content_markdown: str | None = None
    examples: list | None = None
    estimated_minutes: int | None = None
    order: int | None = None


class AdminLessonOut(ORMModel):
    id: str
    phase_id: str
    lesson_number: int
    title: str
    description: str
    content_markdown: str
    examples: list
    estimated_minutes: int
    order: int


class ChallengeIn(BaseModel):
    lesson_id: str
    title: str
    description: str = ""
    starter_code: str = ""
    test_cases: list = []
    difficulty: str = "easy"
    hints: list = []
    solution_code: str = ""
    order: int = 0


class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    starter_code: str | None = None
    test_cases: list | None = None
    difficulty: str | None = None
    hints: list | None = None
    solution_code: str | None = None
    order: int | None = None


class AdminChallengeOut(ORMModel):
    id: str
    lesson_id: str
    title: str
    description: str
    starter_code: str
    test_cases: list
    difficulty: str
    hints: list
    solution_code: str
    order: int


class QuizQuestionIn(BaseModel):
    lesson_id: str
    order: int = 0
    type: str = "multiple-choice"
    text: str
    options: list = []
    correct_answer: str
    explanation: str = ""


class QuizQuestionUpdate(BaseModel):
    order: int | None = None
    type: str | None = None
    text: str | None = None
    options: list | None = None
    correct_answer: str | None = None
    explanation: str | None = None


class AdminQuizQuestionOut(ORMModel):
    id: str
    lesson_id: str
    order: int
    type: str
    text: str
    options: list
    correct_answer: str
    explanation: str


class AdminSubmissionOut(BaseModel):
    id: str
    user_id: str
    user_email: str
    challenge_id: str
    challenge_title: str
    status: str
    score: int
    attempts: int
    submitted_at: datetime


TokenResponse.model_rebuild()
