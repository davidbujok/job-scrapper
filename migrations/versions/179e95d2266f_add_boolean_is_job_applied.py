"""Add boolean is job applied

Revision ID: 179e95d2266f
Revises: c4b5f32265bc
Create Date: 2024-01-25 20:49:37.487533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '179e95d2266f'
down_revision = 'c4b5f32265bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('apply_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_column('apply_status')

    # ### end Alembic commands ###
