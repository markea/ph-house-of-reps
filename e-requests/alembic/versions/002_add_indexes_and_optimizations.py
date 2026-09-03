"""add indexes and optimizations

Revision ID: 002_add_indexes
Revises: 001_initial_schema
Create Date: 2026-09-03 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_indexes'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('requests', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index('idx_requests_requester_status', 'requests', ['requester_id', 'status'])
    op.create_index('idx_requests_service_status', 'requests', ['service_id', 'status'])
    op.create_index('idx_approvals_approver_status', 'request_approvals', ['approver_id', 'status'])

def downgrade() -> None:
    op.drop_index('idx_approvals_approver_status', table_name='request_approvals')
    op.drop_index('idx_requests_service_status', table_name='requests')
    op.drop_index('idx_requests_requester_status', table_name='requests')
    op.drop_column('requests', 'updated_at')
