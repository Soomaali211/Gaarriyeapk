
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ResearchClaim, Source


def create_research_claim(
    db: Session,
    *,
    claim: str,
    researcher: str | None = None,
    source_id: int | None = None,
    page_reference: str | None = None,
) -> ResearchClaim:
    if not claim or not claim.strip():
        raise ValueError("Research claim cannot be empty.")

    if source_id is not None:
        source = db.get(Source, source_id)

        if source is None:
            raise ValueError("Source does not exist.")

    research_claim = ResearchClaim(
        claim=claim.strip(),
        researcher=researcher,
        source_id=source_id,
        page_reference=page_reference,
        status="UNVERIFIED",
    )

    db.add(research_claim)
    db.commit()
    db.refresh(research_claim)

    return research_claim


def get_research_claim(
    db: Session,
    *,
    claim_id: int,
) -> ResearchClaim | None:
    return db.get(ResearchClaim, claim_id)


def list_research_claims(
    db: Session,
    *,
    source_id: int | None = None,
    status: str | None = None,
) -> list[ResearchClaim]:
    statement = select(ResearchClaim)

    if source_id is not None:
        statement = statement.where(
            ResearchClaim.source_id == source_id
        )

    if status is not None:
        statement = statement.where(
            ResearchClaim.status == status
        )

    statement = statement.order_by(ResearchClaim.id)

    return list(db.scalars(statement).all())
  
