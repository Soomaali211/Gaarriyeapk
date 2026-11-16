
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuditLog


def record_audit_log(
    db: Session,
    *,
    entity_type: str,
    entity_id: int,
    action: str,
    old_status: str | None = None,
    new_status: str | None = None,
    actor: str | None = None,
    note: str | None = None,
) -> AuditLog:
    if not entity_type or not entity_type.strip():
        raise ValueError("Entity type cannot be empty.")

    if entity_id <= 0:
        raise ValueError("Entity ID must be positive.")

    if not action or not action.strip():
        raise ValueError("Audit action cannot be empty.")

    audit_log = AuditLog(
        entity_type=entity_type.strip().upper(),
        entity_id=entity_id,
        action=action.strip().upper(),
        old_status=old_status,
        new_status=new_status,
        actor=actor,
        note=note,
    )

    db.add(audit_log)
    db.flush()

    return audit_log


def create_audit_log(
    db: Session,
    *,
    entity_type: str,
    entity_id: int,
    action: str,
    old_status: str | None = None,
    new_status: str | None = None,
    actor: str | None = None,
    note: str | None = None,
) -> AuditLog:
    audit_log = record_audit_log(
        db,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_status=old_status,
        new_status=new_status,
        actor=actor,
        note=note,
    )

    db.commit()
    db.refresh(audit_log)

    return audit_log


def list_audit_logs(
    db: Session,
    *,
    entity_type: str | None = None,
    entity_id: int | None = None,
) -> list[AuditLog]:
    statement = select(AuditLog)

    if entity_type is not None:
        statement = statement.where(
            AuditLog.entity_type == entity_type.strip().upper()
        )

    if entity_id is not None:
        statement = statement.where(
            AuditLog.entity_id == entity_id
        )

    statement = statement.order_by(AuditLog.id.desc())

    return list(db.scalars(statement).all())
