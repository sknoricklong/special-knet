"""create posts table

Revision ID: 5386d41ae443
Revises: 
Create Date: 2023-07-04 11:55:27.639732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5386d41ae443'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("date", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("tags", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('events')
    pass
