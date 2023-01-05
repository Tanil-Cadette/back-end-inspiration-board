"""empty message

Revision ID: 27f444225b03
Revises: c4a672c1a2d2
Create Date: 2023-01-04 20:17:54.482185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27f444225b03'
down_revision = 'c4a672c1a2d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('likes_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'likes_count')
    # ### end Alembic commands ###