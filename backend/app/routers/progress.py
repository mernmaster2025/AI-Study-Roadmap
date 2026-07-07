"""Per-user progress overview for the dashboard."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Challenge, Lesson, Phase, User
from app.progress import (
    _phase_challenge_ids,
    _solved_challenge_ids,
    lessons_with_quiz_in_phase,
    passed_quiz_lesson_ids,
)
from app.schemas import PhaseProgress, ProgressOverview

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress", response_model=ProgressOverview)
def get_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    solved = _solved_challenge_ids(db, current_user.id)
    passed_quizzes = passed_quiz_lesson_ids(db, current_user.id)
    phases = db.scalars(select(Phase).order_by(Phase.order)).all()

    phase_rows: list[PhaseProgress] = []
    total_challenges = 0
    total_solved = 0
    total_quizzes_passed = 0

    for phase in phases:
        challenge_ids = _phase_challenge_ids(db, phase.id)
        solved_here = [c for c in challenge_ids if c in solved]

        lesson_ids = list(
            db.scalars(select(Lesson.id).where(Lesson.phase_id == phase.id)).all()
        )
        # A lesson is complete when all its challenges are solved.
        lessons_completed = 0
        for lid in lesson_ids:
            lch = list(
                db.scalars(
                    select(Challenge.id).where(Challenge.lesson_id == lid)
                ).all()
            )
            if lch and all(c in solved for c in lch):
                lessons_completed += 1

        quiz_lesson_ids = lessons_with_quiz_in_phase(db, phase.id)
        quizzes_passed_here = [lid for lid in quiz_lesson_ids if lid in passed_quizzes]

        total = len(challenge_ids)
        pct = round(100.0 * len(solved_here) / total, 1) if total else 0.0
        total_challenges += total
        total_solved += len(solved_here)
        total_quizzes_passed += len(quizzes_passed_here)

        phase_rows.append(
            PhaseProgress(
                phase_id=phase.id,
                phase_number=phase.phase_number,
                title=phase.title,
                status="completed" if total and len(solved_here) == total else "in_progress",
                lessons_completed=lessons_completed,
                total_lessons=len(lesson_ids),
                challenges_solved=len(solved_here),
                total_challenges=total,
                quizzes_passed=len(quizzes_passed_here),
                total_quizzes=len(quiz_lesson_ids),
                progress_percentage=pct,
            )
        )

    overall = round(100.0 * total_solved / total_challenges, 1) if total_challenges else 0.0
    return ProgressOverview(
        overall_percentage=overall,
        challenges_solved=total_solved,
        quizzes_passed=total_quizzes_passed,
        phases=phase_rows,
    )
