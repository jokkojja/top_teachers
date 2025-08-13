"""create exercises table

Revision ID: 74a4ce70f3ef
Revises: e1b64a46656f
Create Date: 2025-08-12 15:25:22.986526

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "74a4ce70f3ef"
down_revision: Union[str, Sequence[str], None] = "e1b64a46656f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE exercises (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            text VARCHAR(300) NOT NULL,
            author_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            uuid BYTEA NOT NULL

        );
    """)


def downgrade():
    op.execute("DROP TABLE exercises;")
