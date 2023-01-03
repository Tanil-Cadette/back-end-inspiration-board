"""empty message

Revision ID: d93ac62e899f
Revises: 743986718b3d
Create Date: 2023-01-03 13:53:21.558373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd93ac62e899f'
down_revision = '743986718b3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('color', sa.String(), nullable=True))
    op.add_column('card', sa.Column('likes_count', sa.Integer(), nullable=True))
    op.add_column('card', sa.Column('text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'text')
    op.drop_column('card', 'likes_count')
    op.drop_column('card', 'color')
    # ### end Alembic commands ###
