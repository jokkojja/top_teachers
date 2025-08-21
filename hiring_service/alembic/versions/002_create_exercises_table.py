"""create exercises table

Revision ID: 9fc3f9c22845
Revises: 679766339b4e
Create Date: 2025-08-18 14:44:43.231324

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9fc3f9c22845"
down_revision: Union[str, Sequence[str], None] = "679766339b4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE exercises (
            id SERIAL PRIMARY KEY,
            uuid UUID NOT NULL UNIQUE,
            title VARCHAR(100) NOT NULL,
            text VARCHAR(300) NOT NULL
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE exercises CASCADE;")
