"""Read-only content routes: phases, lessons, challenges."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Challenge, Lesson, Phase
from app.schemas import ChallengeOut, LessonOut, PhaseDetail, PhaseOut

router = APIRouter(prefix="/api", tags=["content"])


@router.get("/phases", response_model=list[PhaseOut])
def list_phases(db: Session = Depends(get_db)):
    return db.scalars(select(Phase).order_by(Phase.order)).all()


@router.get("/phases/{phase_id}", response_model=PhaseDetail)
def get_phase(phase_id: str, db: Session = Depends(get_db)):
    phase = db.get(Phase, phase_id)
    if phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


@router.get("/lessons/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/challenges/{challenge_id}", response_model=ChallengeOut)
def get_challenge(challenge_id: str, db: Session = Depends(get_db)):
    challenge = db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge
