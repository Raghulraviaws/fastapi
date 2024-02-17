"""add other columns to posts table

Revision ID: 07c1365d574b
Revises: f461d6fde4c9
Create Date: 2024-02-16 09:26:51.805065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07c1365d574b'
down_revision: Union[str, None] = 'f461d6fde4c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts","created_at")
    pass
