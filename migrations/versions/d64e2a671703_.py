"""empty message

Revision ID: d64e2a671703
Revises: 4bf0fa2bdc87
Create Date: 2023-04-07 14:26:14.131732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64e2a671703'
down_revision = '4bf0fa2bdc87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('title', sa.String(length=200), server_default='', nullable=False))
    op.add_column('article', sa.Column('body', sa.Text(), server_default='', nullable=False))
    op.add_column('article', sa.Column('dt_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('article', sa.Column('dt_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'dt_updated')
    op.drop_column('article', 'dt_created')
    op.drop_column('article', 'body')
    op.drop_column('article', 'title')
    # ### end Alembic commands ###
