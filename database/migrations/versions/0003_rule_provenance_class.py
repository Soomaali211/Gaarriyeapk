"""Add explicit provenance classification to rules."""

from alembic import op
import sqlalchemy as sa

revision = "0003_rule_provenance_class"
down_revision = "0002_audit_logs"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "rules",
        sa.Column(
            "rule_class",
            sa.String(length=40),
            nullable=False,
            server_default="UNCLASSIFIED",
        ),
    )
    op.create_index("ix_rules_rule_class", "rules", ["rule_class"])


def downgrade():
    op.drop_index("ix_rules_rule_class", table_name="rules")
    op.drop_column("rules", "rule_class")
