"""Run + grade a challenge submission, persist it, and update progress."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Challenge, User, UserChallengeSubmission
from app.progress import recompute_phase_progress
from app.schemas import ExecuteCodeRequest, ExecuteCodeResponse
from app.services.code_executor import execute_with_tests

router = APIRouter(prefix="/api", tags=["execute"])


@router.post("/execute-code", response_model=ExecuteCodeResponse)
def execute_code(
    payload: ExecuteCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    challenge = db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")

    result = execute_with_tests(payload.code, challenge.test_cases or [])

    # Count prior attempts so we can increment.
    prior = db.scalars(
        select(UserChallengeSubmission).where(
            UserChallengeSubmission.user_id == current_user.id,
            UserChallengeSubmission.challenge_id == challenge.id,
        )
    ).all()

    submission = UserChallengeSubmission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        submitted_code=payload.code,
        status="passed" if result["all_tests_passed"] else "failed",
        test_results=result["test_results"],
        score=result["score"],
        attempts=len(prior) + 1,
    )
    db.add(submission)
    db.commit()

    # Keep the phase's progress row in sync with the latest results.
    recompute_phase_progress(db, current_user.id, challenge.lesson.phase_id)

    return ExecuteCodeResponse(**result)
