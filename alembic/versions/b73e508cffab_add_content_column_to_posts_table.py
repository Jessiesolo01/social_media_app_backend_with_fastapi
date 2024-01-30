"""add content column to posts table

Revision ID: b73e508cffab
Revises: 0fb23e2de75e
Create Date: 2024-01-30 12:01:50.725068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b73e508cffab'
down_revision: Union[str, None] = '0fb23e2de75e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
