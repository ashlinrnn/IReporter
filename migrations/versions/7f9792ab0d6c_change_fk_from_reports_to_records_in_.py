"""Change FK from reports to records in images and videos

Revision ID: 7f9792ab0d6c
Revises: ab8677eb1768
Create Date: 2026-04-02
"""

from alembic import op
import sqlalchemy as sa


revision = '7f9792ab0d6c'
down_revision = 'ab8677eb1768'
branch_labels = None
depends_on = None


def upgrade():
   
    op.rename_table('reports', 'records')

     
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_constraint('image_record_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'image_record_id_fkey',
            'records',
            ['record_id'],
            ['id']
        )

    
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_constraint('videos_record_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'videos_record_id_fkey',
            'records',
            ['record_id'],
            ['id']
        )


def downgrade():
    
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_constraint('videos_record_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'videos_record_id_fkey',
            'reports',
            ['record_id'],
            ['id']
        )

   
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_constraint('image_record_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'image_record_id_fkey',
            'reports',
            ['record_id'],
            ['id']
        )

    op.rename_table('records', 'reports')