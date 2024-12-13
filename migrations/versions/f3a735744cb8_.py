"""empty message

Revision ID: f3a735744cb8
Revises: e358cd1c99d5
Create Date: 2024-12-01 03:11:06.528407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a735744cb8'
down_revision = 'e358cd1c99d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_fav_id', sa.Integer(), nullable=True),
    sa.Column('user_fav_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_fav_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_fav_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_fav_name', sa.Integer(), nullable=True),
    sa.Column('user_fav_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_fav_name'], ['people.id'], ),
    sa.ForeignKeyConstraint(['user_fav_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_people')
    op.drop_table('favorite_planets')
    # ### end Alembic commands ###
