"""initial schema (users, phases, lessons, challenges, progress, submissions)

Revision ID: 0001
Revises:
Create Date: 2026-07-07
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "phases",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("phase_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("estimated_hours", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_phases_phase_number", "phases", ["phase_number"], unique=True)

    op.create_table(
        "lessons",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("phase_id", sa.String(), sa.ForeignKey("phases.id"), nullable=False),
        sa.Column("lesson_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("content_markdown", sa.Text(), nullable=False),
        sa.Column("examples", sa.JSON(), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_lessons_phase_id", "lessons", ["phase_id"])

    op.create_table(
        "challenges",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("lesson_id", sa.String(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("starter_code", sa.Text(), nullable=False),
        sa.Column("test_cases", sa.JSON(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("hints", sa.JSON(), nullable=False),
        sa.Column("solution_code", sa.Text(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_challenges_lesson_id", "challenges", ["lesson_id"])

    op.create_table(
        "user_progress",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("phase_id", sa.String(), sa.ForeignKey("phases.id"), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("progress_percentage", sa.Float(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("user_id", "phase_id", name="uq_user_phase"),
    )
    op.create_index("ix_user_progress_user_id", "user_progress", ["user_id"])
    op.create_index("ix_user_progress_phase_id", "user_progress", ["phase_id"])

    op.create_table(
        "user_challenge_submissions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("challenge_id", sa.String(), sa.ForeignKey("challenges.id"), nullable=False),
        sa.Column("submitted_code", sa.Text(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("test_results", sa.JSON(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_user_challenge_submissions_user_id", "user_challenge_submissions", ["user_id"]
    )
    op.create_index(
        "ix_user_challenge_submissions_challenge_id",
        "user_challenge_submissions",
        ["challenge_id"],
    )


def downgrade() -> None:
    op.drop_table("user_challenge_submissions")
    op.drop_table("user_progress")
    op.drop_table("challenges")
    op.drop_table("lessons")
    op.drop_table("phases")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
