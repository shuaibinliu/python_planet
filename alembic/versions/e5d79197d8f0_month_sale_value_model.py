"""month sale value model

Revision ID: e5d79197d8f0
Revises: 28614b616429
Create Date: 2018-11-09 17:45:23.213972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5d79197d8f0'
down_revision = '28614b616429'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ProductMonthSaleValue',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('PMSVid', sa.String(length=64), nullable=False),
    sa.Column('PRid', sa.String(length=64), nullable=False),
    sa.Column('PMSVnum', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('PMSVid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ProductMonthSaleValue')
    # ### end Alembic commands ###
