"""'add'

Revision ID: f18aa539f759
Revises: b8c49e5235d4
Create Date: 2019-01-11 01:32:35.508772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f18aa539f759'
down_revision = 'b8c49e5235d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('QuestOutline', sa.Column('QOtype', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('QuestOutline', 'QOtype')
    # ### end Alembic commands ###