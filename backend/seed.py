"""Seed the database with the full 12-phase AI curriculum.

Run:  python seed.py

Idempotent — clears and re-inserts all course content each run so you can
iterate on lessons freely. It does NOT touch users or their submissions.

Content lives in the ``seed_data`` package (one module per phase); this script
just walks ``seed_data.PHASES`` and writes rows, deriving ``order`` from list
position.
"""
from sqlalchemy import delete, func, select

from app.database import Base, SessionLocal, engine
from app.models import (
    Challenge,
    Lesson,
    Phase,
    QuizQuestion,
    UserChallengeSubmission,
    UserProgress,
    UserQuizAttempt,
)
from seed_data import PHASES


def reset_content(db):
    """Wipe all content so it can be re-inserted cleanly.

    Reseeding regenerates content with fresh UUIDs, which would orphan any
    per-user rows that reference the old content ids. Postgres enforces those
    FKs, so we must clear the dependent user rows (submissions, quiz attempts,
    progress) as well. User accounts themselves are preserved.

    Delete order matters: children before parents.
    """
    db.execute(delete(UserChallengeSubmission))
    db.execute(delete(UserQuizAttempt))
    db.execute(delete(UserProgress))
    db.execute(delete(QuizQuestion))
    db.execute(delete(Challenge))
    db.execute(delete(Lesson))
    db.execute(delete(Phase))
    db.commit()


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        reset_content(db)

        n_phases = n_lessons = n_challenges = n_questions = 0

        for p_index, phase_data in enumerate(PHASES):
            phase = Phase(
                phase_number=phase_data["phase_number"],
                title=phase_data["title"],
                description=phase_data["description"],
                estimated_hours=phase_data.get("estimated_hours", 0),
                order=p_index,
            )
            db.add(phase)
            db.flush()  # assign phase.id
            n_phases += 1

            for l_index, lesson_data in enumerate(phase_data["lessons"]):
                lesson = Lesson(
                    phase_id=phase.id,
                    lesson_number=l_index + 1,
                    title=lesson_data["title"],
                    description=lesson_data.get("description", ""),
                    content_markdown=lesson_data.get("content_markdown", "").strip(),
                    examples=lesson_data.get("examples", []),
                    estimated_minutes=lesson_data.get("estimated_minutes", 0),
                    order=l_index,
                )
                db.add(lesson)
                db.flush()
                n_lessons += 1

                # Attach the lesson's quiz (inline in the lesson data).
                quiz = lesson_data.get("quiz", [])
                for q_index, q in enumerate(quiz):
                    db.add(
                        QuizQuestion(
                            lesson_id=lesson.id,
                            order=q_index,
                            type=q.get("type", "multiple-choice"),
                            text=q["text"],
                            options=q.get("options", []),
                            correct_answer=q["correct_answer"],
                            explanation=q.get("explanation", ""),
                        )
                    )
                    n_questions += 1

                for c_index, ch in enumerate(lesson_data.get("challenges", [])):
                    db.add(
                        Challenge(
                            lesson_id=lesson.id,
                            title=ch["title"],
                            description=ch.get("description", ""),
                            starter_code=ch.get("starter_code", ""),
                            test_cases=ch.get("test_cases", []),
                            difficulty=ch.get("difficulty", "easy"),
                            hints=ch.get("hints", []),
                            solution_code=ch.get("solution_code", ""),
                            order=c_index,
                        )
                    )
                    n_challenges += 1

        db.commit()

        total = db.scalar(select(func.count()).select_from(Phase))
        print(
            f"Seeded {n_phases} phases, {n_lessons} lessons, "
            f"{n_challenges} challenges, {n_questions} quiz questions. "
            f"(Phase rows in DB: {total})"
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
