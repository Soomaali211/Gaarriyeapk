from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Source


def create_source(
    db: Session,
    *,
    title: str,
    source_type: str,
    author: str | None = None,
    publication_year: int | None = None,
    locator: str | None = None,
    notes: str | None = None,
) -> Source:
    source = Source(
        title=title,
        author=author,
        publication_year=publication_year,
        source_type=source_type,
        locator=locator,
        notes=notes,
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


def get_source(db: Session, source_id: int) -> Source | None:
    return db.get(Source, source_id)


def list_sources(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    statement = (
        select(Source)
        .order_by(Source.id)
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())
