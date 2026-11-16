
"""Create audit logs table."""

from alembic import op
import sqlalchemy as sa


revision = "0002_audit_logs"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "audit_logs",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "entity_type",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "entity_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "action",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "old_status",
            sa.String(30),
        ),
        sa.Column(
            "new_status",
            sa.String(30),
        ),
        sa.Column(
            "actor",
            sa.String(255),
        ),
        sa.Column(
            "note",
            sa.Text(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_audit_logs_entity_type",
        "audit_logs",
        ["entity_type"],
    )

    op.create_index(
        "ix_audit_logs_entity_id",
        "audit_logs",
        ["entity_id"],
    )


def downgrade():
    op.drop_index(
        "ix_audit_logs_entity_id",
        table_name="audit_logs",
    )

    op.drop_index(
        "ix_audit_logs_entity_type",
        table_name="audit_logs",
    )

    op.drop_table("audit_logs")
  
