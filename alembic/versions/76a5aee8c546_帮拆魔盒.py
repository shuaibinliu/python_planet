"""帮拆魔盒

Revision ID: 76a5aee8c546
Revises: 2248d87dc232
Create Date: 2018-12-05 14:06:47.043039

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '76a5aee8c546'
down_revision = '2248d87dc232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('FreshManFirst',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('FMFAid', sa.String(length=64), nullable=False),
    sa.Column('SUid', sa.String(length=64), nullable=False),
    sa.Column('PRid', sa.String(length=64), nullable=False),
    sa.Column('FMFAstartTime', sa.DateTime(), nullable=False),
    sa.Column('FMFAendTime', sa.DateTime(), nullable=False),
    sa.Column('FMFAstatus', sa.Integer(), nullable=True),
    sa.Column('AgreeStartime', sa.Date(), nullable=True),
    sa.Column('AgreeEndtime', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('FMFAid', 'SUid')
    )
    op.create_table('MagicBoxJoin',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('MBJid', sa.String(length=64), nullable=False),
    sa.Column('USid', sa.String(length=64), nullable=False),
    sa.Column('MBAid', sa.String(length=64), nullable=False),
    sa.Column('MBJprice', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('MBJid')
    )
    op.create_table('MagixBoxOpen',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('MBOid', sa.String(length=64), nullable=False),
    sa.Column('USid', sa.String(length=64), nullable=False),
    sa.Column('MBJid', sa.String(length=64), nullable=False),
    sa.Column('MBOgear', sa.Integer(), nullable=False),
    sa.Column('MBOresult', sa.Float(), nullable=False),
    sa.Column('MBOprice', sa.Float(), nullable=False),
    sa.Column('MBOhasShare', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('MBOid')
    )
    op.create_table('UserInvitation',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('UINid', sa.String(length=64), nullable=False),
    sa.Column('USInviter', sa.String(length=64), nullable=True),
    sa.Column('USInvited', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('UINid')
    )
    op.create_table('UserSalesvolume',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('USVid', sa.String(length=64), nullable=False),
    sa.Column('USid', sa.String(length=64), nullable=True),
    sa.Column('USVamount', sa.DECIMAL(precision=28, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('USVid')
    )
    op.drop_table('magix_box_open')
    op.drop_table('magic_box_join')
    op.alter_column('Supplizer', 'SUname',
               existing_type=mysql.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Supplizer', 'SUname',
               existing_type=mysql.VARCHAR(length=16),
               nullable=False)
    op.create_table('magic_box_join',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('MBJid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('MABid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('MBJprice', mysql.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('MBJid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('magix_box_open',
    sa.Column('isdelete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('createtime', mysql.DATETIME(), nullable=True),
    sa.Column('updatetime', mysql.DATETIME(), nullable=True),
    sa.Column('MBOid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('USid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('MBJid', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('MBOgear', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('MBOresult', mysql.FLOAT(), nullable=False),
    sa.Column('MBOprice', mysql.FLOAT(), nullable=False),
    sa.Column('MBOhasShare', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('MBOid'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('UserSalesvolume')
    op.drop_table('UserInvitation')
    op.drop_table('MagixBoxOpen')
    op.drop_table('MagicBoxJoin')
    op.drop_table('FreshManFirst')
    # ### end Alembic commands ###
