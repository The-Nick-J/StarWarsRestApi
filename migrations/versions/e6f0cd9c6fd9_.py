"""empty message

Revision ID: e6f0cd9c6fd9
Revises: d8e19f402bb7
Create Date: 2024-02-09 17:45:46.242498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6f0cd9c6fd9'
down_revision = 'd8e19f402bb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=True),
    sa.Column('terrain', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_column('birth_year')
        batch_op.drop_column('mass')
        batch_op.drop_column('homeworld_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('mass', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('birth_year', sa.VARCHAR(length=50), autoincrement=False, nullable=True))

    op.drop_table('favorite')
    op.drop_table('planet')
    # ### end Alembic commands ###
