"""empty message

Revision ID: f239e3f83fef
Revises: d4dee8475387
Create Date: 2021-12-11 19:32:56.893432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f239e3f83fef'
down_revision = 'd4dee8475387'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('Day', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'Day')
    # ### end Alembic commands ###
