"""order and pay

Revision ID: ac17508b7ec7
Revises: 307bf4cafc44
Create Date: 2018-11-02 13:40:48.550425

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac17508b7ec7'
down_revision = '307bf4cafc44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderMain', sa.Column('OPayno', sa.String(length=64), nullable=True))
    op.drop_column('OrderMain', 'OPayid')
    op.add_column('OrderPay', sa.Column('OPayno', sa.String(length=64), nullable=True))
    op.drop_column('OrderPay', 'OPsn')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderPay', sa.Column('OPsn', mysql.VARCHAR(collation='utf8_bin', length=64), nullable=True))
    op.drop_column('OrderPay', 'OPayno')
    op.add_column('OrderMain', sa.Column('OPayid', mysql.VARCHAR(collation='utf8_bin', length=64), nullable=True))
    op.drop_column('OrderMain', 'OPayno')
    # ### end Alembic commands ###