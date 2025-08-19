"""create assigments table

Revision ID: 13569d9f79b8
Revises: 9fc3f9c22845
Create Date: 2025-08-18 14:44:48.637045

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "13569d9f79b8"
down_revision: Union[str, Sequence[str], None] = "9fc3f9c22845"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE assignments  (
            id SERIAL PRIMARY KEY,
            candidate_uuid UUID NOT NULL REFERENCES candidates(uuid),
            exercise_uuid UUID NOT NULL REFERENCES exercises(uuid)
        );
    """)


def downgrade():
    op.execute("DROP TABLE assignments CASCADE;")
