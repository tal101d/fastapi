""" add content column to posts table

Revision ID: 6537acd2b276
Revises: b43929a21d02
Create Date: 2023-11-07 22:44:41.484542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6537acd2b276'
down_revision: Union[str, None] = 'b43929a21d02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
