"""create candidate table

Revision ID: a15f7eb64041
Revises: 74a4ce70f3ef
Create Date: 2025-08-15 14:10:48.504453

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a15f7eb64041"
down_revision: Union[str, Sequence[str], None] = "74a4ce70f3ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE candidates (
            id SERIAL PRIMARY KEY,
            uuid UUID NOT NULL UNIQUE
        );
    """)


def downgrade():
    op.execute("DROP TABLE candidates;")
