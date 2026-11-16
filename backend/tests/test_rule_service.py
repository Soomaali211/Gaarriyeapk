
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Rule
from app.rule_service import (
    create_rule,
    add_rule_evidence,
    get_rule_evidence,
    get_verified_rules,
    verify_rule_evidence,
    verify_rule,
)
from app.source_service import create_source


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


def test_new_rule_starts_unverified(db):
    rule = create_rule(
        db,
        code="GABAY-001",
        genre_id="gabay",
        title="Xeer tijaabo ah",
        description="Xeer aan weli la xaqiijin.",
    )

    assert rule.status == "UNVERIFIED"


def test_rule_evidence_starts_unverified(db):
    source = create_source(
        db,
        title="Mahadho",
        author="Gaarriye",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="JIIFTO-001",
        genre_id="jiifto",
        title="Xeer tijaabo ah",
        description="Sharaxaadda xeerka.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        page_reference="Bogga 47",
        quotation="Xigasho tijaabo ah.",
    )

    assert evidence.verification_status == "UNVERIFIED"
    assert evidence.rule_id == rule.id
    assert evidence.source_id == source.id


def test_unverified_rule_is_not_returned(db):
    rule = create_rule(
        db,
        code="GABAY-002",
        genre_id="gabay",
        title="Xeer aan la xaqiijin",
        description="Sharaxaad.",
    )

    rules = get_verified_rules(db, genre_id="gabay")

    assert rule.id not in [item.id for item in rules]


def test_verified_rule_is_returned(db):
    source = create_source(
        db,
        title="Mahadho",
        author="Gaarriye",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="GABAY-003",
        genre_id="gabay",
        title="Xeer la xaqiijiyey",
        description="Sharaxaad.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho laga soo qaatay isha.",
    )

    verify_rule_evidence(
        db,
        evidence_id=evidence.id,
    )

    verify_rule(
        db,
        rule_id=rule.id,
    )

    rules = get_verified_rules(db, genre_id="gabay")

    assert rule.id in [item.id for item in rules]


def test_duplicate_rule_code_is_rejected(db):
    create_rule(
        db,
        code="GABAY-004",
        genre_id="gabay",
        title="Xeerka koowaad",
        description="Sharaxaad.",
    )

    with pytest.raises(ValueError):
        create_rule(
            db,
            code="GABAY-004",
            genre_id="gabay",
            title="Xeer labaad",
            description="Sharaxaad kale.",
        )


def test_evidence_rejects_missing_rule(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    with pytest.raises(ValueError):
        add_rule_evidence(
            db,
            rule_id=999,
            source_id=source.id,
        )


def test_evidence_rejects_missing_source(db):
    rule = create_rule(
        db,
        code="GABAY-005",
        genre_id="gabay",
        title="Xeer tijaabo ah",
        description="Sharaxaad.",
    )

    with pytest.raises(ValueError):
        add_rule_evidence(
            db,
            rule_id=rule.id,
            source_id=999,
        )


def test_get_rule_evidence_returns_correct_records(db):
    source = create_source(
        db,
        title="Mahadho",
        author="Gaarriye",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="JIIFTO-002",
        genre_id="jiifto",
        title="Xeerka Jiiftada",
        description="Sharaxaadda xeerka.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        page_reference="Bogga 47",
        quotation="Xigasho Gaarriye.",
        interpretation="Fasiraad cilmiyeed.",
    )

    results = get_rule_evidence(
        db,
        rule_id=rule.id,
    )

    assert len(results) == 1
    assert results[0].id == evidence.id
    assert results[0].rule_id == rule.id
    assert results[0].source_id == source.id
    assert results[0].page_reference == "Bogga 47"
    assert results[0].quotation == "Xigasho Gaarriye."
    assert results[0].interpretation == "Fasiraad cilmiyeed."
    assert results[0].verification_status == "UNVERIFIED"


def test_get_rule_evidence_does_not_mix_rules(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    first_rule = create_rule(
        db,
        code="JIIFTO-003",
        genre_id="jiifto",
        title="Xeerka koowaad",
        description="Sharaxaad.",
    )

    second_rule = create_rule(
        db,
        code="GABAY-006",
        genre_id="gabay",
        title="Xeerka labaad",
        description="Sharaxaad.",
    )

    add_rule_evidence(
        db,
        rule_id=first_rule.id,
        source_id=source.id,
        page_reference="Bogga 47",
    )

    add_rule_evidence(
        db,
        rule_id=second_rule.id,
        source_id=source.id,
        page_reference="Bogga 58",
    )

    results = get_rule_evidence(
        db,
        rule_id=first_rule.id,
    )

    assert len(results) == 1
    assert results[0].rule_id == first_rule.id
    assert results[0].page_reference == "Bogga 47"


def test_get_rule_evidence_returns_empty_list_for_missing_rule(db):
    results = get_rule_evidence(
        db,
        rule_id=999,
    )

    assert results == []


def test_evidence_without_quotation_cannot_be_verified(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="VERIFY-001",
        genre_id="jiifto",
        title="Xeer tijaabo ah",
        description="Sharaxaad.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
    )

    with pytest.raises(
        ValueError,
        match="source quotation",
    ):
        verify_rule_evidence(
            db,
            evidence_id=evidence.id,
        )

    assert evidence.verification_status == "UNVERIFIED"


def test_evidence_with_quotation_can_be_verified(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="VERIFY-002",
        genre_id="jiifto",
        title="Xeer tijaabo ah",
        description="Sharaxaad.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho tijaabo ah.",
    )

    result = verify_rule_evidence(
        db,
        evidence_id=evidence.id,
    )

    assert result.verification_status == "VERIFIED"


def test_rule_without_verified_evidence_cannot_be_verified(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="VERIFY-003",
        genre_id="jiifto",
        title="Xeer tijaabo ah",
        description="Sharaxaad.",
    )

    add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho tijaabo ah.",
    )

    with pytest.raises(
        ValueError,
        match="verified evidence",
    ):
        verify_rule(
            db,
            rule_id=rule.id,
        )

    assert rule.status == "UNVERIFIED"


def test_rule_with_verified_evidence_can_be_verified(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="VERIFY-004",
        genre_id="gabay",
        title="Xeer la xaqiijinayo",
        description="Sharaxaad.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho tijaabo ah.",
    )

    verify_rule_evidence(
        db,
        evidence_id=evidence.id,
    )

    result = verify_rule(
        db,
        rule_id=rule.id,
    )

    assert result.status == "VERIFIED"


def test_adding_new_evidence_resets_rule_to_unverified(db):
    source = create_source(
        db,
        title="Mahadho",
        source_type="primary_source",
    )

    rule = create_rule(
        db,
        code="VERIFY-005",
        genre_id="gabay",
        title="Xeer tijaabo ah",
        description="Sharaxaad.",
    )

    evidence = add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho koowaad.",
    )

    verify_rule_evidence(
        db,
        evidence_id=evidence.id,
    )

    verify_rule(
        db,
        rule_id=rule.id,
    )

    assert rule.status == "VERIFIED"

    add_rule_evidence(
        db,
        rule_id=rule.id,
        source_id=source.id,
        quotation="Xigasho cusub.",
    )

    assert rule.status == "UNVERIFIED"


def test_verification_rejects_missing_evidence(db):
    with pytest.raises(ValueError):
        verify_rule_evidence(
            db,
            evidence_id=999,
        )


def test_verification_rejects_missing_rule(db):
    with pytest.raises(ValueError):
        verify_rule(
            db,
            rule_id=999,
        )


def test_rule_class_defaults_to_unclassified(db):
    rule = create_rule(
        db,
        code="CLASS-DEFAULT-001",
        genre_id="gabay",
        title="Xeer aan la kala saarin",
        description="Tijaabo.",
    )
    assert rule.rule_class == "UNCLASSIFIED"


def test_invalid_rule_class_is_rejected(db):
    with pytest.raises(ValueError, match="Unsupported rule class"):
        create_rule(
            db,
            code="CLASS-INVALID-001",
            genre_id="gabay",
            title="Xeer khaldan",
            description="Tijaabo.",
            rule_class="GAARRIYE_OR_RESEARCH_MIXED",
        )


def test_registry_returns_only_verified_and_classified_rules(db):
    from app.rule_service import get_verified_rule_registry

    primary = create_rule(
        db,
        code="REG-PRIMARY-001",
        genre_id="jiifto",
        title="Xeerka Gaarriye",
        description="Tijaabo.",
        rule_class="GAARRIYE_PRIMARY",
    )
    researcher = create_rule(
        db,
        code="REG-RESEARCH-001",
        genre_id="jiifto",
        title="Fasiraad cilmi-baare",
        description="Tijaabo.",
        rule_class="RESEARCHER_INTERPRETATION",
    )
    unclassified = create_rule(
        db,
        code="REG-UNCLASSIFIED-001",
        genre_id="jiifto",
        title="Aan la kala saarin",
        description="Tijaabo.",
    )
    primary.status = "VERIFIED"
    researcher.status = "VERIFIED"
    unclassified.status = "VERIFIED"
    db.commit()

    rows = get_verified_rule_registry(db, genre_id="jiifto")
    assert {row.rule_class for row in rows} == {
        "GAARRIYE_PRIMARY",
        "RESEARCHER_INTERPRETATION",
    }
    assert unclassified.id not in {row.id for row in rows}

    only_primary = get_verified_rule_registry(
        db, genre_id="jiifto", rule_class="GAARRIYE_PRIMARY"
    )
    assert [row.id for row in only_primary] == [primary.id]
