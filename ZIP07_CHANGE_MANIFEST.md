# ZIP 07 Change Manifest

- Adds explicit provenance class to Rule model.
- Preserves all pre-existing rule rows as `UNCLASSIFIED`.
- Adds Alembic revision `0003_rule_provenance_class` after `0002_audit_logs`.
- Adds a verified, provenance-filtered read-only registry endpoint.
- Preserves legacy verified-rules endpoint.
- Does not connect registry metadata to executable meter logic.
- Does not alter source records, research claims, frontend, or prior migrations.
- Combined backend test suite: 76 passed.
- Migration upgrade, downgrade to 0002, and re-upgrade tested on SQLite.
