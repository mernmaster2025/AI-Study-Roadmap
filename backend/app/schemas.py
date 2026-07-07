"""Pydantic request/response models for the API."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---- Auth ----
class DevLoginRequest(BaseModel):
    email: EmailStr = "demo@studyplatform.dev"
    name: str = "Demo Learner"


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
    progress_percentage: float


class ProgressOverview(BaseModel):
    overall_percentage: float
    challenges_solved: int
    phases: list[PhaseProgress]


TokenResponse.model_rebuild()
