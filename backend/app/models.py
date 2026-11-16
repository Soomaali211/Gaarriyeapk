from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255))
    publication_year: Mapped[int | None] = mapped_column(Integer)
    source_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    locator: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Rule(Base):
    __tablename__ = "rules"

    # Explicit provenance class; existing records remain UNCLASSIFIED until reviewed.
    rule_class: Mapped[str] = mapped_column(
        String(40), default="UNCLASSIFIED", server_default="UNCLASSIFIED", nullable=False, index=True
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    genre_id: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default="UNVERIFIED",
server_default="UNVERIFIED",
nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class RuleEvidence(Base):
    __tablename__ = "rule_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"), nullable=False, index=True
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"), nullable=False, index=True
    )
    page_reference: Mapped[str | None] = mapped_column(String(100))
    quotation: Mapped[str | None] = mapped_column(Text)
    interpretation: Mapped[str | None] = mapped_column(Text)
    verification_status: Mapped[str] = mapped_column(
        String(30), default="UNVERIFIED",
server_default="UNVERIFIED",
nullable=False,
    )


class ResearchClaim(Base):
    __tablename__ = "research_claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    researcher: Mapped[str | None] = mapped_column(String(255))
    source_id: Mapped[int | None] = mapped_column(
        ForeignKey("sources.id")
    )
    page_reference: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(
        String(30), default="UNVERIFIED",
server_default="UNVERIFIED",
nullable=False,
    )

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    entity_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    old_status: Mapped[str | None] = mapped_column(
        String(30),
    )
    new_status: Mapped[str | None] = mapped_column(
        String(30),
    )
    actor: Mapped[str | None] = mapped_column(
        String(255),
    )
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
