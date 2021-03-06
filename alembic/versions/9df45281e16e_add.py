"""'add'

Revision ID: 9df45281e16e
Revises: fffc57636d09
Create Date: 2018-11-07 11:18:09.975134

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9df45281e16e'
down_revision = 'fffc57636d09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('identifyingcode', 'ICtime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('identifyingcode', sa.Column('ICtime', mysql.DATETIME(), nullable=False))
    # ### end Alembic commands ###
