import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.audit_service import (
    create_audit_log,
    list_audit_logs,
)


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


def test_create_audit_log(db):
    log = create_audit_log(
        db,
        entity_type="rule",
        entity_id=1,
        action="verification",
        old_status="UNVERIFIED",
        new_status="VERIFIED",
        actor="admin",
        note="Source evidence reviewed.",
    )

    assert log.id is not None
    assert log.entity_type == "RULE"
    assert log.entity_id == 1
    assert log.action == "VERIFICATION"
    assert log.old_status == "UNVERIFIED"
    assert log.new_status == "VERIFIED"
    assert log.actor == "admin"
    assert log.note == "Source evidence reviewed."
    assert log.created_at is not None


def test_audit_log_rejects_empty_entity_type(db):
    with pytest.raises(ValueError):
        create_audit_log(
            db,
            entity_type=" ",
            entity_id=1,
            action="UPDATE",
        )


def test_audit_log_rejects_invalid_entity_id(db):
    with pytest.raises(ValueError):
        create_audit_log(
            db,
            entity_type="RULE",
            entity_id=0,
            action="UPDATE",
        )


def test_audit_log_rejects_empty_action(db):
    with pytest.raises(ValueError):
        create_audit_log(
            db,
            entity_type="RULE",
            entity_id=1,
            action=" ",
        )


def test_list_audit_logs_returns_all_records(db):
    create_audit_log(
        db,
        entity_type="RULE",
        entity_id=1,
        action="CREATE",
    )

    create_audit_log(
        db,
        entity_type="RULE_EVIDENCE",
        entity_id=2,
        action="VERIFY",
    )

    results = list_audit_logs(db)

    assert len(results) == 2


def test_list_audit_logs_filters_by_entity_type(db):
    create_audit_log(
        db,
        entity_type="RULE",
        entity_id=1,
        action="CREATE",
    )

    create_audit_log(
        db,
        entity_type="RULE_EVIDENCE",
        entity_id=2,
        action="VERIFY",
    )

    results = list_audit_logs(
        db,
        entity_type="rule",
    )

    assert len(results) == 1
    assert results[0].entity_type == "RULE"


def test_list_audit_logs_filters_by_entity_id(db):
    create_audit_log(
        db,
        entity_type="RULE",
        entity_id=1,
        action="CREATE",
    )

    create_audit_log(
        db,
        entity_type="RULE",
        entity_id=2,
        action="VERIFY",
    )

    results = list_audit_logs(
        db,
        entity_id=2,
    )

    assert len(results) == 1
    assert results[0].entity_id == 2


def test_audit_logs_are_returned_newest_first(db):
    first = create_audit_log(
        db,
        entity_type="RULE",
        entity_id=1,
        action="CREATE",
    )

    second = create_audit_log(
        db,
        entity_type="RULE",
        entity_id=1,
        action="VERIFY",
    )

    results = list_audit_logs(db)

    assert results[0].id == second.id
    assert results[1].id == first.id
  
