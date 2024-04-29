"""Add modified_time column to video table

Revision ID: 29d00712a68c
Revises: a8e74313876c
Create Date: 2024-04-28 12:55:39.387160

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '29d00712a68c'
down_revision = 'a8e74313876c'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modified_time', sa.DateTime(), nullable=True))

def downgrade():
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.drop_column('modified_time')
