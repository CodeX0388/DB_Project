"""Create indexes

Revision ID: e917a5581ef1
Revises: 397e6bc77921
Create Date: 2023-12-27 22:28:14.401606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e917a5581ef1'
down_revision = '397e6bc77921'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('index_new_column1', 'ships', ['new_column1'], unique=False)

def downgrade():
    op.drop_index('index_new_column1', table_name='ships')
