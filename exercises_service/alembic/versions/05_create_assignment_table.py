"""create assignment table

Revision ID: efd2efdd908f
Revises: a15f7eb64041
Create Date: 2025-08-15 14:11:02.051351

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "efd2efdd908f"
down_revision: Union[str, Sequence[str], None] = "a15f7eb64041"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE assignment  (
            id SERIAL PRIMARY KEY,
            candidate_uuid UUID NOT NULL REFERENCES candidates(uuid),
            exercise_uuid UUID NOT NULL REFERENCES exercises(uuid)
        );
    """)


def downgrade():
    op.execute("DROP TABLE assignment CASCADE;")
