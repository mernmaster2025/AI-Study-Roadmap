"""add users.password_hash for email/password login

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-07
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("password_hash", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "password_hash")
