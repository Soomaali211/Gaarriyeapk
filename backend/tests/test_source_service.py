from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.source_service import (
    create_source,
    get_source,
    list_sources,
)


def test_source_can_be_created_and_retrieved():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as db:
            source = create_source(
                db,
                title="Mahadho",
                author="Gaarriye",
                publication_year=1976,
                source_type="primary_source",
                locator="Bogga 47",
            )

            assert source.id is not None
            assert source.title == "Mahadho"
            assert source.author == "Gaarriye"

            retrieved = get_source(db, source.id)

            assert retrieved is not None
            assert retrieved.title == "Mahadho"

            sources = list_sources(db)

            assert len(sources) == 1
            assert sources[0].title == "Mahadho"

    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
