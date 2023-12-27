"""Add new columns

Revision ID: 397e6bc77921
Revises: 
Create Date: 2023-12-27 22:24:42.697880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '397e6bc77921'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('ships', sa.Column('new_column1', sa.String(), nullable=True))
    op.add_column('ships', sa.Column('new_column2', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('ships', 'new_column1')
    op.drop_column('ships', 'new_column2')
