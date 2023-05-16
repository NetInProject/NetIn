"""Agrega columna 'image' a la tabla 'publication'

Revision ID: 87f51f1d9aa9
Revises: 600fbfc19e36
Create Date: 2023-05-15 19:15:28.651465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87f51f1d9aa9'
down_revision = '600fbfc19e36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publication', sa.Column('image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publication', 'image')
    # ### end Alembic commands ###