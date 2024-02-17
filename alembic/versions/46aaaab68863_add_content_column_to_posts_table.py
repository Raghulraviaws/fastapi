"""add content column to posts table

Revision ID: 46aaaab68863
Revises: 11aa1a79d381
Create Date: 2024-02-16 09:08:09.864586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46aaaab68863'
down_revision: Union[str, None] = '11aa1a79d381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
