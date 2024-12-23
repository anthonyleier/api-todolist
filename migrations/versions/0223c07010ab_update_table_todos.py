"""update table todos

Revision ID: 0223c07010ab
Revises: 21df5470d5db
Create Date: 2024-11-13 14:25:00.624205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0223c07010ab'
down_revision: Union[str, None] = '21df5470d5db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('todos', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'updated_at')
    op.drop_column('todos', 'created_at')
    # ### end Alembic commands ###
