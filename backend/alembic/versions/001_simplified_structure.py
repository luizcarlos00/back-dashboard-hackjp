"""Simplified database structure

Revision ID: 001_simplified
Revises: 
Create Date: 2025-11-09 05:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '001_simplified'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('device_id', sa.String(length=255), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('idade', sa.Integer(), nullable=True),
        sa.Column('interesses', sa.JSON(), nullable=True),
        sa.Column('nivel_educacional', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('last_active_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_device_id'), 'users', ['device_id'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create contents table
    op.create_table('contents',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('publico_alvo', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contents_title'), 'contents', ['title'], unique=False)
    op.create_index(op.f('ix_contents_publico_alvo'), 'contents', ['publico_alvo'], unique=False)
    op.create_index(op.f('ix_contents_category'), 'contents', ['category'], unique=False)
    op.create_index(op.f('ix_contents_is_active'), 'contents', ['is_active'], unique=False)
    
    # Create videos table
    op.create_table('videos',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('content_id', sa.String(length=36), nullable=False),
        sa.Column('video_id', sa.String(length=255), nullable=False),  # ID do YouTube
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('quantity_until_e2e', sa.Integer(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['content_id'], ['contents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_videos_content_id'), 'videos', ['content_id'], unique=False)
    
    # Create activities table
    op.create_table('activities',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('content_id', sa.String(length=36), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['content_id'], ['contents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activities_content_id'), 'activities', ['content_id'], unique=False)
    
    # Create user_video_progress table
    op.create_table('user_video_progress',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('video_id', sa.String(length=36), nullable=False),
        sa.Column('watched', sa.Boolean(), nullable=True),
        sa.Column('watched_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_video_progress_user_id'), 'user_video_progress', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_video_progress_video_id'), 'user_video_progress', ['video_id'], unique=False)
    op.create_index(op.f('ix_user_video_progress_watched_at'), 'user_video_progress', ['watched_at'], unique=False)
    
    # Create user_activity_responses table
    op.create_table('user_activity_responses',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('activity_id', sa.String(length=36), nullable=False),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('grau_aprendizagem', sa.Float(), nullable=True),
        sa.Column('responded', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_activity_responses_user_id'), 'user_activity_responses', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_activity_responses_activity_id'), 'user_activity_responses', ['activity_id'], unique=False)
    op.create_index(op.f('ix_user_activity_responses_created_at'), 'user_activity_responses', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (to respect foreign keys)
    op.drop_index(op.f('ix_user_activity_responses_created_at'), table_name='user_activity_responses')
    op.drop_index(op.f('ix_user_activity_responses_activity_id'), table_name='user_activity_responses')
    op.drop_index(op.f('ix_user_activity_responses_user_id'), table_name='user_activity_responses')
    op.drop_table('user_activity_responses')
    
    op.drop_index(op.f('ix_user_video_progress_watched_at'), table_name='user_video_progress')
    op.drop_index(op.f('ix_user_video_progress_video_id'), table_name='user_video_progress')
    op.drop_index(op.f('ix_user_video_progress_user_id'), table_name='user_video_progress')
    op.drop_table('user_video_progress')
    
    op.drop_index(op.f('ix_activities_content_id'), table_name='activities')
    op.drop_table('activities')
    
    op.drop_index(op.f('ix_videos_content_id'), table_name='videos')
    op.drop_table('videos')
    
    op.drop_index(op.f('ix_contents_is_active'), table_name='contents')
    op.drop_index(op.f('ix_contents_category'), table_name='contents')
    op.drop_index(op.f('ix_contents_publico_alvo'), table_name='contents')
    op.drop_index(op.f('ix_contents_title'), table_name='contents')
    op.drop_table('contents')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_device_id'), table_name='users')
    op.drop_table('users')

