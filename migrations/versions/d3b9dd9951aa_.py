"""empty message

Revision ID: d3b9dd9951aa
Revises: 2c4720d60296
Create Date: 2019-01-29 11:16:54.964783

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd3b9dd9951aa'
down_revision = '2c4720d60296'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member_comment', 'score')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member_comment', sa.Column('score', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='评分'))
    # ### end Alembic commands ###
