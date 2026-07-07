"""quiz tables (quiz_questions, user_quiz_attempts)

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-07
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("lesson_id", sa.String(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
    )
    op.create_index("ix_quiz_questions_lesson_id", "quiz_questions", ["lesson_id"])

    op.create_table(
        "user_quiz_attempts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("lesson_id", sa.String(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_user_quiz_attempts_user_id", "user_quiz_attempts", ["user_id"])
    op.create_index("ix_user_quiz_attempts_lesson_id", "user_quiz_attempts", ["lesson_id"])


def downgrade() -> None:
    op.drop_table("user_quiz_attempts")
    op.drop_table("quiz_questions")
