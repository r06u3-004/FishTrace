"""add intel result uniqueness

Revision ID: c3f5a1d9b742
Revises: f49482bc6da8
Create Date: 2026-11-26 22:15:00.000000
"""

from collections.abc import Sequence

from sqlalchemy import text

from alembic import op

revision: str = "c3f5a1d9b742"
down_revision: str | None = "f49482bc6da8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

CONSTRAINT_NAME = "uq_intel_results_indicator_provider_queried"


def upgrade() -> None:
    duplicate = (
        op.get_bind()
        .execute(
            text(
                """
            SELECT 1
            FROM intel_results
            GROUP BY indicator_id, provider, queried_at
            HAVING COUNT(*) > 1
            LIMIT 1
            """
            )
        )
        .first()
    )
    if duplicate is not None:
        raise RuntimeError("Cannot add intel_results uniqueness: duplicate rows detected")
    op.create_unique_constraint(CONSTRAINT_NAME, "intel_results", ["indicator_id", "provider", "queried_at"])


def downgrade() -> None:
    op.drop_constraint(CONSTRAINT_NAME, "intel_results", type_="unique")
