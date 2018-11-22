"""优惠券字段

Revision ID: d2684f69dfbb
Revises: 7ccde67e8aaf
Create Date: 2018-11-22 17:57:27.819325

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd2684f69dfbb'
down_revision = '7ccde67e8aaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('OrderRefundFlow',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('ORFid', sa.String(length=64), nullable=False),
    sa.Column('ORAid', sa.String(length=64), nullable=False),
    sa.Column('ORAmount', sa.Float(), nullable=False),
    sa.Column('OPayno', sa.String(length=64), nullable=False),
    sa.Column('OPayType', sa.String(length=64), nullable=True),
    sa.Column('ORFoutRequestNo', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('ORFid')
    )
    op.create_table('supplizer',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('SUid', sa.String(length=64), nullable=False),
    sa.Column('SUname', sa.String(length=16), nullable=False),
    sa.Column('SUlinkman', sa.String(length=16), nullable=False),
    sa.Column('SUlinkPhone', sa.String(length=11), nullable=False),
    sa.Column('SUaddress', sa.String(length=255), nullable=False),
    sa.Column('SUstatus', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('SUid')
    )
    op.drop_table('IndexBrandProduct')
    op.drop_table('IndexBrand')
    op.drop_table('IndexHotProduct')
    op.add_column('Coupon', sa.Column('COremainNum', sa.Integer(), nullable=True))
    op.alter_column('User', 'UStelphone',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=13),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('User', 'UStelphone',
               existing_type=mysql.VARCHAR(collation='utf8_bin', length=13),
               nullable=True)
    op.drop_column('Coupon', 'COremainNum')
    op.create_table('IndexHotProduct',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('IHPid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('PRid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('IHPsort', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('IHPid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('IndexBrand',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('IBid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('PBid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('IBsort', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('IBid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('IndexBrandProduct',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('IBPid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('PRid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('IBPsort', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('IBPid', 'PRid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('supplizer')
    op.drop_table('OrderRefundFlow')
    # ### end Alembic commands ###
