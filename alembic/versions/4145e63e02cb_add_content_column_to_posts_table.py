"""add content column to posts table

Revision ID: 4145e63e02cb
Revises: cef2c1e6f977
Create Date: 2022-09-13 02:38:47.355540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4145e63e02cb'
down_revision = 'cef2c1e6f977'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
