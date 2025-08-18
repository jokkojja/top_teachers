"""create candidates table

Revision ID: 679766339b4e
Revises:
Create Date: 2025-08-18 14:44:33.524176

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "679766339b4e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE candidates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            uuid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid()
        );
    """)


def downgrade():
    op.execute("DROP TABLE candidates CASCADE;")
