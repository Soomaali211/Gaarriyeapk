
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Rule, RuleEvidence, Source
from app.audit_service import record_audit_log

RULE_CLASSES = {
    "GAARRIYE_PRIMARY",
    "RESEARCHER_INTERPRETATION",
    "COMPATIBLE_OTHER_RULE",
    "UNCLASSIFIED",
}


def create_rule(
    db: Session,
    *,
    code: str,
    genre_id: str,
    title: str,
    description: str,
    rule_class: str = "UNCLASSIFIED",
) -> Rule:
    if rule_class not in RULE_CLASSES:
        raise ValueError("Unsupported rule class.")

    existing = db.scalar(
        select(Rule).where(Rule.code == code)
    )

    if existing:
        raise ValueError("Rule code already exists.")

    rule = Rule(
        code=code,
        genre_id=genre_id,
        title=title,
        description=description,
        rule_class=rule_class,
        status="UNVERIFIED",
    )

    db.add(rule)
    db.flush()

    record_audit_log(
        db,
        entity_type="RULE",
        entity_id=rule.id,
        action="CREATED",
        new_status="UNVERIFIED",
        note="Rule created.",
    )

    db.commit()
    db.refresh(rule)

    return rule


def add_rule_evidence(
    db: Session,
    *,
    rule_id: int,
    source_id: int,
    page_reference: str | None = None,
    quotation: str | None = None,
    interpretation: str | None = None,
) -> RuleEvidence:
    rule = db.get(Rule, rule_id)
    source = db.get(Source, source_id)

    if rule is None:
        raise ValueError("Rule does not exist.")

    if source is None:
        raise ValueError("Source does not exist.")

    old_rule_status = rule.status

    # New evidence requires the rule to be reviewed again.
    rule.status = "UNVERIFIED"

    evidence = RuleEvidence(
        rule_id=rule_id,
        source_id=source_id,
        page_reference=page_reference,
        quotation=quotation,
        interpretation=interpretation,
        verification_status="UNVERIFIED",
    )

    db.add(evidence)
    db.flush()

    record_audit_log(
        db,
        entity_type="RULE_EVIDENCE",
        entity_id=evidence.id,
        action="CREATED",
        new_status="UNVERIFIED",
        note="Rule evidence added.",
    )

    if old_rule_status != "UNVERIFIED":
        record_audit_log(
            db,
            entity_type="RULE",
            entity_id=rule.id,
            action="STATUS_RESET",
            old_status=old_rule_status,
            new_status="UNVERIFIED",
            note="New evidence requires rule review.",
        )

    db.commit()
    db.refresh(evidence)

    return evidence


def verify_rule_evidence(
    db: Session,
    *,
    evidence_id: int,
) -> RuleEvidence:
    evidence = db.get(RuleEvidence, evidence_id)

    if evidence is None:
        raise ValueError("Rule evidence does not exist.")

    if not evidence.quotation or not evidence.quotation.strip():
        raise ValueError(
            "Evidence must contain a source quotation."
        )

    old_status = evidence.verification_status
    evidence.verification_status = "VERIFIED"

    record_audit_log(
        db,
        entity_type="RULE_EVIDENCE",
        entity_id=evidence.id,
        action="VERIFIED",
        old_status=old_status,
        new_status="VERIFIED",
        note="Evidence marked verified after review.",
    )

    db.commit()
    db.refresh(evidence)

    return evidence


def verify_rule(
    db: Session,
    *,
    rule_id: int,
) -> Rule:
    rule = db.get(Rule, rule_id)

    if rule is None:
        raise ValueError("Rule does not exist.")

    statement = (
        select(RuleEvidence)
        .where(
            RuleEvidence.rule_id == rule_id,
            RuleEvidence.verification_status == "VERIFIED",
        )
    )

    verified_evidence = list(
        db.scalars(statement).all()
    )

    if not verified_evidence:
        raise ValueError(
            "Rule requires at least one verified evidence."
        )

    old_status = rule.status
    rule.status = "VERIFIED"

    record_audit_log(
        db,
        entity_type="RULE",
        entity_id=rule.id,
        action="VERIFIED",
        old_status=old_status,
        new_status="VERIFIED",
        note="Rule marked verified after evidence review.",
    )

    db.commit()
    db.refresh(rule)

    return rule


def get_rule_evidence(
    db: Session,
    *,
    rule_id: int,
) -> list[RuleEvidence]:
    statement = (
        select(RuleEvidence)
        .where(RuleEvidence.rule_id == rule_id)
        .order_by(RuleEvidence.id)
    )

    return list(db.scalars(statement).all())


def get_verified_rules(
    db: Session,
    *,
    genre_id: str,
) -> list[Rule]:
    statement = (
        select(Rule)
        .where(
            Rule.genre_id == genre_id,
            Rule.status == "VERIFIED",
        )
        .order_by(Rule.id)
    )

    return list(db.scalars(statement).all())


def get_verified_rule_registry(
    db: Session,
    *,
    genre_id: str | None = None,
    rule_class: str | None = None,
) -> list[Rule]:
    """Return only reviewed rules with an explicit provenance class.

    This registry is descriptive metadata only. It does not make a rule
    executable by the meter engine.
    """
    if rule_class is not None and rule_class not in RULE_CLASSES - {"UNCLASSIFIED"}:
        raise ValueError("Unsupported rule class.")

    statement = select(Rule).where(
        Rule.status == "VERIFIED",
        Rule.rule_class != "UNCLASSIFIED",
    )
    if genre_id is not None:
        statement = statement.where(Rule.genre_id == genre_id)
    if rule_class is not None:
        statement = statement.where(Rule.rule_class == rule_class)
    statement = statement.order_by(Rule.genre_id, Rule.rule_class, Rule.id)
    return list(db.scalars(statement).all())
