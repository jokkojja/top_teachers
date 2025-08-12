"""create users table

Revision ID: e1b64a46656f
Revises:
Create Date: 2025-08-12 14:50:37.483073

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e1b64a46656f"
down_revision: Union[str, Sequence[str], None] = "2fcbdca17f39"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            role_id INTEGER NOT NULL REFERENCES roles(id),
            token BYTEA NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

        );
    """)


def downgrade():
    op.execute("DROP TABLE users;")
