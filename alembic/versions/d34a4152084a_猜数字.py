"""猜数字

Revision ID: d34a4152084a
Revises: 799df421cc4a
Create Date: 2018-11-23 13:39:10.452528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd34a4152084a'
down_revision = '799df421cc4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CorrectNum',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('CNid', sa.String(length=64), nullable=False),
    sa.Column('CNnum', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('CNid')
    )
    op.create_table('GuessNum',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('GNid', sa.String(length=64), nullable=False),
    sa.Column('GNnum', sa.String(length=16), nullable=False),
    sa.Column('USid', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('GNid')
    )
    op.create_table('TrialCommodity',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('TCid', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('TCid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TrialCommodity')
    op.drop_table('GuessNum')
    op.drop_table('CorrectNum')
    # ### end Alembic commands ###
