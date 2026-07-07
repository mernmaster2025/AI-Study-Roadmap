"""Quiz routes: fetch a lesson's quiz (answers hidden) and grade a submission."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Lesson, QuizQuestion, User, UserQuizAttempt
from app.schemas import (
    QuizOut,
    QuizQuestionResult,
    QuizResult,
    QuizSubmission,
)

router = APIRouter(prefix="/api", tags=["quizzes"])

PASS_THRESHOLD = 80


def _normalize(answer: str) -> str:
    """Case/space-insensitive comparison for fill-in-the-blank answers."""
    return answer.strip().lower()


@router.get("/lessons/{lesson_id}/quiz", response_model=QuizOut)
def get_quiz(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    questions = db.scalars(
        select(QuizQuestion)
        .where(QuizQuestion.lesson_id == lesson_id)
        .order_by(QuizQuestion.order)
    ).all()
    return QuizOut(lesson_id=lesson_id, questions=questions)


@router.post("/lessons/{lesson_id}/quiz/submit", response_model=QuizResult)
def submit_quiz(
    lesson_id: str,
    payload: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    questions = db.scalars(
        select(QuizQuestion)
        .where(QuizQuestion.lesson_id == lesson_id)
        .order_by(QuizQuestion.order)
    ).all()
    if not questions:
        raise HTTPException(status_code=404, detail="This lesson has no quiz")

    detailed: list[QuizQuestionResult] = []
    correct_count = 0
    for q in questions:
        user_answer = payload.answers.get(q.id)
        is_correct = (
            user_answer is not None
            and _normalize(user_answer) == _normalize(q.correct_answer)
        )
        if is_correct:
            correct_count += 1
        detailed.append(
            QuizQuestionResult(
                id=q.id,
                text=q.text,
                user_answer=user_answer,
                correct_answer=q.correct_answer,
                correct=is_correct,
                explanation=q.explanation,
            )
        )

    total = len(questions)
    score = round(100 * correct_count / total)

    prior = db.scalars(
        select(UserQuizAttempt).where(
            UserQuizAttempt.user_id == current_user.id,
            UserQuizAttempt.lesson_id == lesson_id,
        )
    ).all()
    db.add(
        UserQuizAttempt(
            user_id=current_user.id,
            lesson_id=lesson_id,
            answers=payload.answers,
            score=score,
            attempts=len(prior) + 1,
        )
    )
    db.commit()

    return QuizResult(
        score=score,
        passed=score >= PASS_THRESHOLD,
        correct_count=correct_count,
        total=total,
        attempts=len(prior) + 1,
        detailed_results=detailed,
    )
