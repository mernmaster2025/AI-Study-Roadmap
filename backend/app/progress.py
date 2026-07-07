"""Progress computation shared by the execute and progress routes.

A challenge counts as *solved* when the learner has at least one passing
submission for it. A phase's progress % is solved-challenges / total-challenges.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Challenge,
    Lesson,
    Phase,
    QuizQuestion,
    UserChallengeSubmission,
    UserProgress,
    UserQuizAttempt,
)


def _solved_challenge_ids(db: Session, user_id: str) -> set[str]:
    rows = db.scalars(
        select(UserChallengeSubmission.challenge_id).where(
            UserChallengeSubmission.user_id == user_id,
            UserChallengeSubmission.status == "passed",
        )
    ).all()
    return set(rows)


PASS_THRESHOLD = 80


def passed_quiz_lesson_ids(db: Session, user_id: str) -> set[str]:
    """Lessons where the user has at least one quiz attempt scoring >= 80."""
    rows = db.scalars(
        select(UserQuizAttempt.lesson_id).where(
            UserQuizAttempt.user_id == user_id,
            UserQuizAttempt.score >= PASS_THRESHOLD,
        )
    ).all()
    return set(rows)


def lessons_with_quiz_in_phase(db: Session, phase_id: str) -> list[str]:
    """Distinct lesson ids in a phase that actually have quiz questions."""
    rows = db.scalars(
        select(QuizQuestion.lesson_id)
        .join(Lesson, QuizQuestion.lesson_id == Lesson.id)
        .where(Lesson.phase_id == phase_id)
        .distinct()
    ).all()
    return list(rows)


def _phase_challenge_ids(db: Session, phase_id: str) -> list[str]:
    return list(
        db.scalars(
            select(Challenge.id)
            .join(Lesson, Challenge.lesson_id == Lesson.id)
            .where(Lesson.phase_id == phase_id)
        ).all()
    )


def recompute_phase_progress(db: Session, user_id: str, phase_id: str) -> UserProgress:
    """Upsert the UserProgress row for (user, phase) from current submissions."""
    challenge_ids = _phase_challenge_ids(db, phase_id)
    solved = _solved_challenge_ids(db, user_id)
    solved_in_phase = [c for c in challenge_ids if c in solved]

    total = len(challenge_ids)
    pct = round(100.0 * len(solved_in_phase) / total, 1) if total else 0.0
    done = total > 0 and len(solved_in_phase) == total

    progress = db.scalar(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.phase_id == phase_id,
        )
    )
    if progress is None:
        progress = UserProgress(user_id=user_id, phase_id=phase_id)
        db.add(progress)

    progress.progress_percentage = pct
    progress.status = "completed" if done else "in_progress"
    progress.completed_at = datetime.now(timezone.utc) if done else None
    db.commit()
    db.refresh(progress)
    return progress
