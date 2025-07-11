"""added ao_website to update_requests

Revision ID: b2db07a0e3a7
Revises: 5b56bd54a1a1
Create Date: 2025-05-05 14:27:40.943339

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2db07a0e3a7"
down_revision: Union[str, None] = "5b56bd54a1a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("update_requests", sa.Column("ao_website", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("update_requests", "ao_website")
    # ### end Alembic commands ###
