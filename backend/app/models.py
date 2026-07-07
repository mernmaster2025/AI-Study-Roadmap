"""ORM models for the Phase-1 vertical slice.

Only the tables the slice actually exercises are defined here (User, Phase,
Lesson, Challenge, UserProgress, UserChallengeSubmission). The full schema from
the spec — Projects, Quizzes, submissions, etc. — slots in alongside these using
the same patterns as we grow beyond Phase 1.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)

    progress: Mapped[list["UserProgress"]] = relationship(back_populates="user")
    submissions: Mapped[list["UserChallengeSubmission"]] = relationship(
        back_populates="user"
    )


class Phase(Base):
    __tablename__ = "phases"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    phase_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    estimated_hours: Mapped[int] = mapped_column(Integer, default=0)
    order: Mapped[int] = mapped_column(Integer, default=0)

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="phase", order_by="Lesson.order"
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    phase_id: Mapped[str] = mapped_column(ForeignKey("phases.id"), index=True)
    lesson_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    content_markdown: Mapped[str] = mapped_column(Text, default="")
    # list of {title, language, code}
    examples: Mapped[list] = mapped_column(JSON, default=list)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=0)
    order: Mapped[int] = mapped_column(Integer, default=0)

    phase: Mapped["Phase"] = relationship(back_populates="lessons")
    challenges: Mapped[list["Challenge"]] = relationship(
        back_populates="lesson", order_by="Challenge.order"
    )


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    lesson_id: Mapped[str] = mapped_column(ForeignKey("lessons.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    starter_code: Mapped[str] = mapped_column(Text, default="")
    # list of {inputs: <repr>, expected: <repr>} — see code_executor
    test_cases: Mapped[list] = mapped_column(JSON, default=list)
    difficulty: Mapped[str] = mapped_column(String, default="easy")
    hints: Mapped[list] = mapped_column(JSON, default=list)
    solution_code: Mapped[str] = mapped_column(Text, default="")
    order: Mapped[int] = mapped_column(Integer, default=0)

    lesson: Mapped["Lesson"] = relationship(back_populates="challenges")


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "phase_id"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    phase_id: Mapped[str] = mapped_column(ForeignKey("phases.id"), index=True)
    status: Mapped[str] = mapped_column(String, default="in_progress")
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="progress")


class UserChallengeSubmission(Base):
    __tablename__ = "user_challenge_submissions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    challenge_id: Mapped[str] = mapped_column(ForeignKey("challenges.id"), index=True)
    submitted_code: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="failed")  # passed / failed
    test_results: Mapped[list] = mapped_column(JSON, default=list)
    score: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=1)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=_now)

    user: Mapped["User"] = relationship(back_populates="submissions")
