"""Initial schema — SQLAlchemy ORM migration

Revision ID: 001
Create Date: 2025-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(150), unique=True, nullable=False),
        sa.Column('password', sa.String(256), nullable=False),
        sa.Column('role', sa.Enum('student','alumni','admin'), default='student'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('email_verified', sa.Boolean(), default=False),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('cover_url', sa.String(500)),
        sa.Column('google_id', sa.String(100), unique=True),
        sa.Column('linkedin_id', sa.String(100), unique=True),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('last_login', sa.DateTime()),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_role',  'users', ['role'])

    op.create_table('students',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('department', sa.String(100)),
        sa.Column('year', sa.String(10)),
        sa.Column('skills', sa.Text()),
        sa.Column('interests', sa.Text()),
        sa.Column('bio', sa.Text()),
        sa.Column('github_url', sa.String(255)),
        sa.Column('linkedin_url', sa.String(255)),
        sa.Column('resume_url', sa.String(500)),
        sa.Column('ai_score', sa.Integer(), default=0),
        sa.Column('placement_score', sa.Integer(), default=0),
        sa.Column('skills_embedding', sa.Text()),
    )

    op.create_table('alumni',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('graduation_year', sa.SmallInteger()),
        sa.Column('company', sa.String(150)),
        sa.Column('job_role', sa.String(150)),
        sa.Column('skills', sa.Text()),
        sa.Column('location', sa.String(100)),
        sa.Column('linkedin', sa.String(255)),
        sa.Column('github_url', sa.String(255)),
        sa.Column('bio', sa.Text()),
        sa.Column('rating', sa.Numeric(3, 2)),
        sa.Column('mentorship_score', sa.Integer(), default=0),
        sa.Column('impact_score', sa.Integer(), default=0),
        sa.Column('is_hiring', sa.Boolean(), default=False),
        sa.Column('mentorship_slots', sa.Integer(), default=3),
        sa.Column('domain', sa.String(100)),
        sa.Column('skills_embedding', sa.Text()),
    )
    op.create_index('ix_alumni_company',  'alumni', ['company'])
    op.create_index('ix_alumni_job_role', 'alumni', ['job_role'])

    op.create_table('mentorship_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False),
        sa.Column('alumni_id', sa.Integer(), sa.ForeignKey('alumni.id', ondelete='CASCADE'), nullable=False),
        sa.Column('message', sa.Text()),
        sa.Column('status', sa.Enum('pending','accepted','rejected'), default='pending'),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.UniqueConstraint('student_id', 'alumni_id', name='uq_request'),
    )

    op.create_table('posts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('image_url', sa.String(500)),
        sa.Column('post_type', sa.Enum('text','image','video','achievement','job'), default='text'),
        sa.Column('tags', sa.String(500)),
        sa.Column('likes_count', sa.Integer(), default=0),
        sa.Column('comments_count', sa.Integer(), default=0),
        sa.Column('shares_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime()),
    )

    op.create_table('notifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(50)),
        sa.Column('title', sa.String(200)),
        sa.Column('message', sa.Text()),
        sa.Column('link', sa.String(500)),
        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime()),
    )
    op.create_index('ix_notifications_user_id', 'notifications', ['user_id'])


def downgrade():
    op.drop_table('notifications')
    op.drop_table('posts')
    op.drop_table('mentorship_requests')
    op.drop_table('alumni')
    op.drop_table('students')
    op.drop_table('users')
