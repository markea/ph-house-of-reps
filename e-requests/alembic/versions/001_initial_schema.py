"""initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # 2. Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('department_id', sa.String(length=36), nullable=True),
        sa.Column('position', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # 3. Service Catalogs table
    op.create_table(
        'service_catalogs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('department_id', sa.String(length=36), nullable=False),
        sa.Column('service_name', sa.String(length=150), nullable=False),
        sa.Column('service_code', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('sla_hours', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('form_schema', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('service_code')
    )

    # 4. Requests table
    op.create_table(
        'requests',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('tracking_number', sa.String(length=50), nullable=False),
        sa.Column('requester_id', sa.String(length=36), nullable=False),
        sa.Column('service_id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('form_data', sa.JSON(), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('sla_deadline', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('csat_rating', sa.Integer(), nullable=True),
        sa.Column('csat_comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['service_id'], ['service_catalogs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tracking_number')
    )

    # 5. Request Approvals table
    op.create_table(
        'request_approvals',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('request_id', sa.String(length=36), nullable=False),
        sa.Column('approver_id', sa.String(length=36), nullable=False),
        sa.Column('step_sequence', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('digital_stamp', sa.String(length=255), nullable=True),
        sa.Column('action_timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('request_id', sa.String(length=36), nullable=True),
        sa.Column('actor_email', sa.String(length=120), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('request_approvals')
    op.drop_table('requests')
    op.drop_table('service_catalogs')
    op.drop_table('users')
    op.drop_table('departments')
