"""订单逆向操作

Revision ID: 37e66b0c8e53
Revises: 63a3654b74cd
Create Date: 2018-11-07 17:46:39.030117

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '37e66b0c8e53'
down_revision = '63a3654b74cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('OrderPart', sa.Column('OPisinORA', sa.Boolean(), nullable=True))
    op.drop_column('OrderPart', 'OPstatus')
    op.add_column('OrderRefundApply', sa.Column('ORAnote', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('OrderRefundApply', 'ORAnote')
    op.add_column('OrderPart', sa.Column('OPstatus', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('OrderPart', 'OPisinORA')
    # ### end Alembic commands ###
