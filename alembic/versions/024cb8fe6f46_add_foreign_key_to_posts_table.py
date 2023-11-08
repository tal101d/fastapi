""" add foreign-key to posts table

Revision ID: 024cb8fe6f46
Revises: 21ecf2fd1ef4
Create Date: 2023-11-07 23:19:19.515838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '024cb8fe6f46'
down_revision: Union[str, None] = '21ecf2fd1ef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', 
        source_table='posts', 
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
