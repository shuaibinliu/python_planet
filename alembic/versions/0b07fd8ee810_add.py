"""'add'

Revision ID: 0b07fd8ee810
Revises: 6cdc44c9a59b
Create Date: 2018-11-09 21:40:37.111474

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0b07fd8ee810'
down_revision = '6cdc44c9a59b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserMetia',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('UMid', sa.String(length=64), nullable=False),
    sa.Column('USid', sa.String(length=64), nullable=True),
    sa.Column('UMurl', sa.Text(), nullable=True),
    sa.Column('UMtype', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('UMid')
    )
    op.drop_table('NewsImage')
    op.drop_table('NewsTrample')
    op.drop_table('NewsTag')
    op.drop_table('NewsFavorite')
    op.drop_table('NewsComment')
    op.drop_table('News')
    op.drop_table('NewsVideo')
    op.drop_column('UserAddress', 'AAid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserAddress', sa.Column('AAid', mysql.VARCHAR(length=8), nullable=False))
    op.create_table('NewsVideo',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NVid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NVvideo', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('NVid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('News',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NEid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NEtitle', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('NEtext', mysql.TEXT(), nullable=True),
    sa.Column('NEstatus', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('NEpageviews', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('NEsort', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('NEid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('NewsComment',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NCid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NEid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NCtext', mysql.VARCHAR(length=140), nullable=True),
    sa.Column('NCparentid', mysql.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('NCid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('NewsFavorite',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NEFid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NEid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('NEFid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('NewsTag',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NTid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NEid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('ITid', mysql.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('NTid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('NewsTrample',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NETid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NEid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('NETid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('NewsImage',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('NIid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('NIimage', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('NIid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('UserMetia')
    # ### end Alembic commands ###