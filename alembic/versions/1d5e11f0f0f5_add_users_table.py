"""add users table

Revision ID: 1d5e11f0f0f5
Revises: b73e508cffab
Create Date: 2024-01-30 12:13:28.678206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d5e11f0f0f5'
down_revision: Union[str, None] = 'b73e508cffab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')       
                    )                 
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
