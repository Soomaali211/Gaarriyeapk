# ZIP 07 — Installation Guide (Android / GitHub)

## Required order

ZIP 01 → ZIP 02 → ZIP 03 → ZIP 04 → ZIP 05 → ZIP 06 → ZIP 07.

ZIP 07 assumes ZIP 03 and ZIP 05 are already integrated. It is an incremental update, not a full repository replacement.

## Exact file actions

| ZIP path | Repository path | Action |
|---|---|---|
| `backend/app/models.py` | `backend/app/models.py` | UPDATE |
| `backend/app/rule_service.py` | `backend/app/rule_service.py` | UPDATE |
| `backend/app/main.py` | `backend/app/main.py` | UPDATE |
| `backend/tests/test_rule_service.py` | `backend/tests/test_rule_service.py` | UPDATE |
| `backend/tests/test_api.py` | `backend/tests/test_api.py` | UPDATE |
| `database/migrations/versions/0003_rule_provenance_class.py` | same path | NEW |
| `docs/integration/ZIP07_RULE_REGISTRY.md` | same path | NEW |

Do not delete or replace `0001_initial_schema.py`, `0002_audit_logs.py`, existing source/research CSVs, frontend files, or other services.

## Android phone workflow

1. Download this ZIP to the phone and extract it with the Files app.
2. Open the private GitHub repository in Chrome and enable **Desktop site**.
3. For each `UPDATE` file, open the matching repository path, choose Edit, replace the complete file content with the ZIP version, and commit the change.
4. For each `NEW` file, navigate to the listed folder and use Add file → Create new file (or upload the extracted file if GitHub offers that option).
5. Keep the exact folder names and migration filename. Do not upload the ZIP itself in place of its contents.
6. Apply the migration only after the code files are committed.

## Migration commands (run in the backend deployment/build environment)

```bash
alembic -c backend/alembic.ini upgrade head
```

Rollback only this migration if necessary:

```bash
alembic -c backend/alembic.ini downgrade 0002_audit_logs
```

Then restore it with `upgrade head`. Do not manually delete database columns.

## Verification

From the repository root:

```bash
cd backend
PYTHONPATH=. pytest -q
```

Expected ZIP 07 combined backend test result in the supplied test workspace: 76 passed.

The new endpoint is `GET /api/v1/rules/registry`. It returns verified rules with explicit provenance classes, but marks `engine_executable` as `false`. Do not expect the meter engine to calculate weights after this ZIP alone.

## Important

This ZIP has been tested against the supplied repository baseline plus ZIP 03 and ZIP 05. ZIP 06 is a frontend integration package and does not change these backend files. No remote GitHub repository has been modified by preparing this ZIP.
