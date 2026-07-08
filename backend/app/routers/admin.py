"""Admin API — everything the admin panel manages.

Every route requires an admin JWT (see require_admin). Grouped as:
  - GET  /api/admin/stats
  - users:        list / update (name, is_admin) / delete
  - submissions:  recent challenge submissions
  - content CRUD: phases, lessons, challenges, quiz questions

Unlike the public content API, admin content responses include the answers
(test_cases, solution_code, correct_answer) so they can be edited.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database import get_db
from app.models import (
    Challenge,
    Lesson,
    Phase,
    QuizQuestion,
    User,
    UserChallengeSubmission,
    UserQuizAttempt,
)
from app.schemas import (
    AdminChallengeOut,
    AdminLessonOut,
    AdminPhaseOut,
    AdminQuizQuestionOut,
    AdminStats,
    AdminSubmissionOut,
    AdminUserOut,
    ChallengeIn,
    ChallengeUpdate,
    LessonIn,
    LessonUpdate,
    PhaseIn,
    PhaseUpdate,
    QuizQuestionIn,
    QuizQuestionUpdate,
    UserUpdate,
)

router = APIRouter(
    prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)]
)


def _count(db: Session, model) -> int:
    return db.scalar(select(func.count()).select_from(model)) or 0


# ---------- stats ----------
@router.get("/stats", response_model=AdminStats)
def stats(db: Session = Depends(get_db)):
    return AdminStats(
        users=_count(db, User),
        admins=db.scalar(select(func.count()).select_from(User).where(User.is_admin)) or 0,
        phases=_count(db, Phase),
        lessons=_count(db, Lesson),
        challenges=_count(db, Challenge),
        quiz_questions=_count(db, QuizQuestion),
        submissions=_count(db, UserChallengeSubmission),
        passed_submissions=db.scalar(
            select(func.count()).select_from(UserChallengeSubmission).where(
                UserChallengeSubmission.status == "passed"
            )
        ) or 0,
        quiz_attempts=_count(db, UserQuizAttempt),
    )


# ---------- users ----------
@router.get("/users", response_model=list[AdminUserOut])
def list_users(
    q: str | None = Query(None, description="search email or name"),
    db: Session = Depends(get_db),
):
    stmt = select(User).order_by(User.created_at.desc())
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(
            func.lower(User.email).like(like) | func.lower(User.name).like(like)
        )
    users = db.scalars(stmt.limit(500)).all()
    return [
        AdminUserOut(
            id=u.id, email=u.email, name=u.name, is_admin=u.is_admin,
            avatar_url=u.avatar_url, created_at=u.created_at,
            has_password=u.password_hash is not None,
        )
        for u in users
    ]


@router.patch("/users/{user_id}", response_model=AdminUserOut)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = payload.model_dump(exclude_unset=True)
    if "is_admin" in data and data["is_admin"] is False and user.id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot remove your own admin rights.")
    for k, v in data.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return AdminUserOut(
        id=user.id, email=user.email, name=user.name, is_admin=user.is_admin,
        avatar_url=user.avatar_url, created_at=user.created_at,
        has_password=user.password_hash is not None,
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account.")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Remove dependent rows first (no cascade configured).
    db.query(UserChallengeSubmission).filter_by(user_id=user_id).delete()
    db.query(UserQuizAttempt).filter_by(user_id=user_id).delete()
    from app.models import UserProgress
    db.query(UserProgress).filter_by(user_id=user_id).delete()
    db.delete(user)
    db.commit()


# ---------- submissions ----------
@router.get("/submissions", response_model=list[AdminSubmissionOut])
def list_submissions(
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(UserChallengeSubmission, User.email, Challenge.title)
        .join(User, UserChallengeSubmission.user_id == User.id)
        .join(Challenge, UserChallengeSubmission.challenge_id == Challenge.id)
        .order_by(UserChallengeSubmission.submitted_at.desc())
        .limit(limit)
    ).all()
    return [
        AdminSubmissionOut(
            id=s.id, user_id=s.user_id, user_email=email,
            challenge_id=s.challenge_id, challenge_title=title,
            status=s.status, score=s.score, attempts=s.attempts,
            submitted_at=s.submitted_at,
        )
        for s, email, title in rows
    ]


# ---------- phases ----------
@router.get("/phases", response_model=list[AdminPhaseOut])
def list_phases(db: Session = Depends(get_db)):
    phases = db.scalars(select(Phase).order_by(Phase.order)).all()
    out = []
    for p in phases:
        n = db.scalar(
            select(func.count()).select_from(Lesson).where(Lesson.phase_id == p.id)
        ) or 0
        item = AdminPhaseOut.model_validate(p)
        item.lesson_count = n
        out.append(item)
    return out


@router.post("/phases", response_model=AdminPhaseOut, status_code=201)
def create_phase(payload: PhaseIn, db: Session = Depends(get_db)):
    phase = Phase(**payload.model_dump())
    db.add(phase)
    db.commit()
    db.refresh(phase)
    return AdminPhaseOut.model_validate(phase)  # lesson_count defaults to 0


@router.patch("/phases/{phase_id}", response_model=AdminPhaseOut)
def update_phase(phase_id: str, payload: PhaseUpdate, db: Session = Depends(get_db)):
    phase = db.get(Phase, phase_id)
    if phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(phase, k, v)
    db.commit()
    db.refresh(phase)
    n = db.scalar(select(func.count()).select_from(Lesson).where(Lesson.phase_id == phase.id)) or 0
    item = AdminPhaseOut.model_validate(phase)
    item.lesson_count = n
    return item


@router.delete("/phases/{phase_id}", status_code=204)
def delete_phase(phase_id: str, db: Session = Depends(get_db)):
    phase = db.get(Phase, phase_id)
    if phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    lesson_ids = list(db.scalars(select(Lesson.id).where(Lesson.phase_id == phase_id)).all())
    if lesson_ids:
        db.query(Challenge).filter(Challenge.lesson_id.in_(lesson_ids)).delete(synchronize_session=False)
        db.query(QuizQuestion).filter(QuizQuestion.lesson_id.in_(lesson_ids)).delete(synchronize_session=False)
        db.query(Lesson).filter(Lesson.phase_id == phase_id).delete(synchronize_session=False)
    db.delete(phase)
    db.commit()


# ---------- lessons ----------
@router.get("/phases/{phase_id}/lessons", response_model=list[AdminLessonOut])
def list_lessons(phase_id: str, db: Session = Depends(get_db)):
    return db.scalars(
        select(Lesson).where(Lesson.phase_id == phase_id).order_by(Lesson.order)
    ).all()


@router.get("/lessons/{lesson_id}", response_model=AdminLessonOut)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/lessons", response_model=AdminLessonOut, status_code=201)
def create_lesson(payload: LessonIn, db: Session = Depends(get_db)):
    lesson = Lesson(**payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.patch("/lessons/{lesson_id}", response_model=AdminLessonOut)
def update_lesson(lesson_id: str, payload: LessonUpdate, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(lesson, k, v)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/lessons/{lesson_id}", status_code=204)
def delete_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.query(Challenge).filter_by(lesson_id=lesson_id).delete()
    db.query(QuizQuestion).filter_by(lesson_id=lesson_id).delete()
    db.delete(lesson)
    db.commit()


# ---------- challenges ----------
@router.get("/lessons/{lesson_id}/challenges", response_model=list[AdminChallengeOut])
def list_challenges(lesson_id: str, db: Session = Depends(get_db)):
    return db.scalars(
        select(Challenge).where(Challenge.lesson_id == lesson_id).order_by(Challenge.order)
    ).all()


@router.post("/challenges", response_model=AdminChallengeOut, status_code=201)
def create_challenge(payload: ChallengeIn, db: Session = Depends(get_db)):
    ch = Challenge(**payload.model_dump())
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


@router.patch("/challenges/{challenge_id}", response_model=AdminChallengeOut)
def update_challenge(challenge_id: str, payload: ChallengeUpdate, db: Session = Depends(get_db)):
    ch = db.get(Challenge, challenge_id)
    if ch is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(ch, k, v)
    db.commit()
    db.refresh(ch)
    return ch


@router.delete("/challenges/{challenge_id}", status_code=204)
def delete_challenge(challenge_id: str, db: Session = Depends(get_db)):
    ch = db.get(Challenge, challenge_id)
    if ch is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    db.query(UserChallengeSubmission).filter_by(challenge_id=challenge_id).delete()
    db.delete(ch)
    db.commit()


# ---------- quiz questions ----------
@router.get("/lessons/{lesson_id}/quiz", response_model=list[AdminQuizQuestionOut])
def list_quiz(lesson_id: str, db: Session = Depends(get_db)):
    return db.scalars(
        select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id).order_by(QuizQuestion.order)
    ).all()


@router.post("/quiz", response_model=AdminQuizQuestionOut, status_code=201)
def create_quiz(payload: QuizQuestionIn, db: Session = Depends(get_db)):
    q = QuizQuestion(**payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.patch("/quiz/{question_id}", response_model=AdminQuizQuestionOut)
def update_quiz(question_id: str, payload: QuizQuestionUpdate, db: Session = Depends(get_db)):
    q = db.get(QuizQuestion, question_id)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(q, k, v)
    db.commit()
    db.refresh(q)
    return q


@router.delete("/quiz/{question_id}", status_code=204)
def delete_quiz(question_id: str, db: Session = Depends(get_db)):
    q = db.get(QuizQuestion, question_id)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
