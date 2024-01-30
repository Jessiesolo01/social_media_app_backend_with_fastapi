"""ccreate posts table

Revision ID: 0fb23e2de75e
Revises: 
Create Date: 2024-01-30 11:40:12.815393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fb23e2de75e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True), 
                    sa.Column("title", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
