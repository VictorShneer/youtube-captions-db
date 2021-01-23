"""caption model

Revision ID: 90e5d645a215
Revises: d48d5a00e9f4
Create Date: 2021-01-23 00:47:59.960773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e5d645a215'
down_revision = 'd48d5a00e9f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caption',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=True),
    sa.Column('start', sa.Float(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('video_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('caption')
    # ### end Alembic commands ###