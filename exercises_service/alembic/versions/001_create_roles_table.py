"""create roles table

Revision ID: 2fcbdca17f39
Revises: e1b64a46656f
Create Date: 2025-08-12 14:51:44.747592

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "2fcbdca17f39"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE roles (
            id SERIAL PRIMARY KEY,
            role VARCHAR(10) NOT NULL UNIQUE
        );
    """)

    op.execute("""
        INSERT INTO roles (role)
        VALUES ('manager'), ('admin')
        ON CONFLICT (role) DO NOTHING;
    """)


def downgrade() -> None:
    op.execute("DROP TABLE roles;")
