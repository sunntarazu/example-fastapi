"""add user table

Revision ID: 1136faebfefa
Revises: 4145e63e02cb
Create Date: 2022-09-13 02:52:01.191111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1136faebfefa'
down_revision = '4145e63e02cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
