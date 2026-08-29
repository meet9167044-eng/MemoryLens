"""Phase 9: create relationships table

Revision ID: a3f9c1d2e456
Revises: da56e6aa5749
Create Date: 2026-08-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3f9c1d2e456'
down_revision = 'da56e6aa5749'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum type first
    relationship_type = postgresql.ENUM(
        'shared_entity', 'shared_tag', 'semantic',
        name='relationship_type'
    )
    relationship_type.create(op.get_bind())

    op.create_table(
        'relationships',
        sa.Column('id',          postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id',   postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('memories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_id',   postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('memories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rel_type',    sa.Enum('shared_entity', 'shared_tag', 'semantic',
                                         name='relationship_type'), nullable=False),
        sa.Column('score',       sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('explanation', sa.String(512), nullable=True),
        sa.Column('created_at',  sa.DateTime(timezone=True),
                  nullable=False, server_default=sa.func.now()),
    )

    # Indexes for fast lookups
    op.create_index('ix_relationships_source_id', 'relationships', ['source_id'])
    op.create_index('ix_relationships_target_id', 'relationships', ['target_id'])

    # Unique constraint: prevent duplicate undirected pairs with same type
    op.create_unique_constraint(
        'uq_relationship_pair_type',
        'relationships',
        ['source_id', 'target_id', 'rel_type'],
    )


def downgrade() -> None:
    op.drop_table('relationships')
    op.execute("DROP TYPE IF EXISTS relationship_type")
