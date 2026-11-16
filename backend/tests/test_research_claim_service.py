
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Source
from app.research_claim_service import (
    create_research_claim,
    get_research_claim,
    list_research_claims,
)


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


def create_test_source(db):
    source = Source(
        title="Mahadho",
        author="Gaarriye",
        source_type="primary_source",
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


def test_create_research_claim(db):
    source = create_test_source(db)

    claim = create_research_claim(
        db,
        claim="Shaqalladu waxay door ku leeyihiin miisaanka.",
        researcher="Cilmi-baare",
        source_id=source.id,
        page_reference="Bogga 47",
    )

    assert claim.id is not None
    assert claim.claim == (
        "Shaqalladu waxay door ku leeyihiin miisaanka."
    )
    assert claim.researcher == "Cilmi-baare"
    assert claim.source_id == source.id
    assert claim.page_reference == "Bogga 47"
    assert claim.status == "UNVERIFIED"


def test_research_claim_without_source(db):
    claim = create_research_claim(
        db,
        claim="Sheegasho aan weli il loo xirin.",
    )

    assert claim.id is not None
    assert claim.source_id is None
    assert claim.status == "UNVERIFIED"


def test_create_research_claim_rejects_empty_claim(db):
    with pytest.raises(
        ValueError,
        match="Research claim cannot be empty.",
    ):
        create_research_claim(
            db,
            claim="   ",
        )


def test_create_research_claim_rejects_missing_source(db):
    with pytest.raises(
        ValueError,
        match="Source does not exist.",
    ):
        create_research_claim(
            db,
            claim="Sheegasho tijaabo ah.",
            source_id=999,
        )


def test_get_research_claim(db):
    created = create_research_claim(
        db,
        claim="Sheegasho cilmiyeed.",
        researcher="Cilmi-baare",
    )

    result = get_research_claim(
        db,
        claim_id=created.id,
    )

    assert result is not None
    assert result.id == created.id
    assert result.claim == "Sheegasho cilmiyeed."


def test_get_missing_research_claim_returns_none(db):
    result = get_research_claim(
        db,
        claim_id=999,
    )

    assert result is None


def test_list_research_claims_returns_all(db):
    create_research_claim(
        db,
        claim="Sheegashada koowaad.",
    )

    create_research_claim(
        db,
        claim="Sheegashada labaad.",
    )

    claims = list_research_claims(db)

    assert len(claims) == 2


def test_list_research_claims_filters_by_source(db):
    source_one = create_test_source(db)

    source_two = Source(
        title="Afrah",
        author="Cilmi-baare",
        source_type="scholarly_source",
    )
    db.add(source_two)
    db.commit()
    db.refresh(source_two)

    create_research_claim(
        db,
        claim="Sheegashada koowaad.",
        source_id=source_one.id,
    )

    create_research_claim(
        db,
        claim="Sheegashada labaad.",
        source_id=source_two.id,
    )

    claims = list_research_claims(
        db,
        source_id=source_one.id,
    )

    assert len(claims) == 1
    assert claims[0].source_id == source_one.id


def test_list_research_claims_filters_by_status(db):
    claim = create_research_claim(
        db,
        claim="Sheegasho aan la xaqiijin.",
    )

    claims = list_research_claims(
        db,
        status="UNVERIFIED",
    )

    assert len(claims) == 1
    assert claims[0].id == claim.id

    verified_claims = list_research_claims(
        db,
        status="VERIFIED",
    )

    assert verified_claims == []
