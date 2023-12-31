"""auto-upvote

Revision ID: 726072c139c1
Revises: 4ff6a0f42421
Create Date: 2023-07-04 13:11:04.360309

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '726072c139c1'
down_revision = '4ff6a0f42421'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upvotes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    op.alter_column('events', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.alter_column('events', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.create_table('evaluations',
    sa.Column('course_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('prof_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('term', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('course_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('course_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('instructor_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('academic_rigor', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('lecture_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('discussion_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('reading_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('assignment_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('accurate_description', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('diverse_perspectives', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('needs_diverse_perspectives', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('needs_international_perspective', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('new_thinking', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('class_time_effective', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('discussion_managed_effectively', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('feedback_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('encourages_diverse_perspectives', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('accessible_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('treats_students_respectfully', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('workload_rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('n_respondents', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='evaluations_pkey')
    )
    op.create_table('professors',
    sa.Column('prof_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('gender', sa.CHAR(length=1), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fall_2023', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='professors_pkey')
    )
    op.drop_table('upvotes')
    # ### end Alembic commands ###
