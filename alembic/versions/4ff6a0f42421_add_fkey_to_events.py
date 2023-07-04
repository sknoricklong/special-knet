"""add fkey to events

Revision ID: 4ff6a0f42421
Revises: c599d643fe77
Create Date: 2023-07-04 13:02:49.990469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ff6a0f42421'
down_revision = 'c599d643fe77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "events",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key('events_users_fk', source_table="events", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('events') as batch_op:
        batch_op.drop_constraint('events_users_fk', type_='foreignkey')
        batch_op.drop_column('user_id')
