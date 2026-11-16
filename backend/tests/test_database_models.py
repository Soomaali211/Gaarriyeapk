from app.database import Base
from app import models


def test_all_database_models_are_registered():
    expected_tables = {
        "sources",
        "rules",
        "rule_evidence",
        "research_claims",
    }

    assert expected_tables.issubset(
        set(Base.metadata.tables.keys())
    )


def test_rules_are_linked_to_evidence():
    evidence_table = Base.metadata.tables["rule_evidence"]

    foreign_keys = {
        fk.target_fullname
        for fk in evidence_table.foreign_keys
    }

    assert "rules.id" in foreign_keys
    assert "sources.id" in foreign_keys

def test_rules_and_evidence_default_to_unverified():
    rule_status = Base.metadata.tables["rules"].c.status
    evidence_status = Base.metadata.tables[
        "rule_evidence"
    ].c.verification_status
    claim_status = Base.metadata.tables[
        "research_claims"
    ].c.status

    for column in (
        rule_status,
        evidence_status,
        claim_status,
    ):
        assert column.default.arg == "UNVERIFIED"
        assert column.server_default is not None
