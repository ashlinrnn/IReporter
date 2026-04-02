"""Add images table and fix record_type enum

Revision ID: 57875ef56f6c
Revises: 758602caa726
Create Date: 2026-04-02 11:05:23.448376
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '57875ef56f6c'
down_revision = '758602caa726'
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table(
        'image',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['record_id'], ['reports.id']),
        sa.PrimaryKeyConstraint('id')
    )

   
    record_type = postgresql.ENUM('red flag', 'intervention', name='record_type')
    record_type.create(op.get_bind(), checkfirst=True)

   
    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.alter_column(
            'type',
            existing_type=sa.String(),       
            type_=record_type,               
            existing_nullable=False,
            postgresql_using="type::record_type"  
        )


def downgrade():
 
    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.alter_column(
            'type',
            existing_type=postgresql.ENUM('red flag', 'intervention', name='record_type'),
            type_=sa.String(),
            existing_nullable=False,
            postgresql_using="type::text"  # cast back to string
        )

    
    op.drop_table('image')

    
    record_type = postgresql.ENUM('red flag', 'intervention', name='record_type')
    record_type.drop(op.get_bind(), checkfirst=True)