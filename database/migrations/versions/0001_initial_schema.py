"""Create initial Gaarriye database schema."""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("author", sa.String(255)),
        sa.Column("publication_year", sa.Integer()),
        sa.Column("source_type", sa.String(100), nullable=False),
        sa.Column("locator", sa.String(255)),
        sa.Column("notes", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_table(
        "rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(100), nullable=False, unique=True),
        sa.Column("genre_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="UNVERIFIED",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )
    op.create_index("ix_rules_genre_id", "rules", ["genre_id"])

    op.create_table(
        "rule_evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("rule_id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("page_reference", sa.String(100)),
        sa.Column("quotation", sa.Text()),
        sa.Column("interpretation", sa.Text()),
        sa.Column(
            "verification_status",
            sa.String(30),
            nullable=False,
            server_default="UNVERIFIED",
        ),
        sa.ForeignKeyConstraint(["rule_id"], ["rules.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
    )
    op.create_index(
        "ix_rule_evidence_rule_id",
        "rule_evidence",
        ["rule_id"],
    )
    op.create_index(
        "ix_rule_evidence_source_id",
        "rule_evidence",
        ["source_id"],
    )

    op.create_table(
        "research_claims",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("researcher", sa.String(255)),
        sa.Column("source_id", sa.Integer()),
        sa.Column("page_reference", sa.String(100)),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="UNVERIFIED",
        ),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
    )


def downgrade():
    op.drop_table("research_claims")

    op.drop_index(
        "ix_rule_evidence_source_id",
        table_name="rule_evidence",
    )
    op.drop_index(
        "ix_rule_evidence_rule_id",
        table_name="rule_evidence",
    )
    op.drop_table("rule_evidence")

    op.drop_index("ix_rules_genre_id", table_name="rules")
    op.drop_table("rules")

    op.drop_table("sources")
