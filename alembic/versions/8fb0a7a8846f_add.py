"""'add'

Revision ID: 8fb0a7a8846f
Revises: 994be0019948
Create Date: 2019-03-21 21:05:07.406386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8fb0a7a8846f'
down_revision = '994be0019948'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CompanyMessage',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('CMid', sa.String(length=64), nullable=False),
    sa.Column('CMtitle', sa.String(length=255), nullable=False),
    sa.Column('CMmessage', mysql.LONGTEXT(), nullable=False),
    sa.Column('CMindex', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('CMid')
    )
    op.create_table('UserWords',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('UWid', sa.String(length=64), nullable=False),
    sa.Column('UWmessage', sa.Text(), nullable=False),
    sa.Column('UWname', sa.String(length=64), nullable=True),
    sa.Column('UWtelphone', sa.String(length=14), nullable=True),
    sa.Column('UWemail', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('UWid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserWords')
    op.drop_table('CompanyMessage')
    # ### end Alembic commands ###
