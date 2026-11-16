# ZIP 01 — Repository Baseline Audit

## Scope
This audit was performed against the uploaded archive `gaarriye-metre-analyzer-main (1).zip`.
It describes only the contents of that archive. It does not claim that the remote GitHub repository
has been changed or that a deployed service or APK has been tested.

## Existing structure
- `frontend/`: `index.html`, `styles.css`, `app.js`, and README.
- `backend/app/`: FastAPI entry point, database setup, SQLAlchemy models, source/rule/research/audit
  services, and conservative phonology inspection.
- `backend/tests/`: seven test modules.
- `database/migrations/`: Alembic environment and migrations `0001_initial_schema.py` and
  `0002_audit_logs.py`.
- `.github/workflows/`: backend CI and GitHub Pages deployment workflows.
- `docs/`: architecture, research, rules, and sources guidance.

## Baseline verification performed
- Backend test suite: **61 passed**.
- Alembic SQLite migration: **0001_initial** and **0002_audit_logs** both applied successfully.
- JavaScript syntax: `node --check frontend/app.js` passed.
- These checks were performed on an extracted copy of the uploaded ZIP.

## Findings that affect integration
1. The API endpoint `POST /api/v1/analyze` deliberately returns `501 ENGINE_NOT_READY`.
   It does not calculate a poetry meter.
2. `POST /api/v1/phonology/inspect` is an orthographic inspection endpoint only. It explicitly
   does not assign metrical weights or issue a meter verdict.
3. The frontend already includes the three independent analysis switches:
   Gaarriye, researchers, and other compatible rules. The interface currently sends choices to
   the API, but no functioning meter engine re-analyzes the text.
4. Frontend persistence is browser `localStorage`; this is not yet IndexedDB/offline database sync.
5. A duplicate file exists at `backend/backend/app/research_claim_service.py`. Its contents are
   byte-for-byte identical to `backend/app/research_claim_service.py`. Do not delete it until
   checking how it entered the repository and whether any deployment/import path uses it.
6. GitHub Pages workflow uses `actions/configure-pages@v5`. This archive cannot establish whether
   Pages is enabled or whether the private repository's plan/settings permit deployment.
7. No Capacitor/Android project, APK build workflow, or APK artifact is present in this archive.

## Integration principles
- Preserve all existing files and behavior unless a reviewed change explicitly requires modification.
- Do not create parallel copies of existing services.
- Keep Alembic migration history linear; add new migrations rather than editing applied migrations.
- Keep Gaarriye primary rules, researcher interpretations, and other compatible rules separately
  identified in data and analysis results.
- Unverified material must never produce a verified meter verdict.
- Keep `ENGINE_NOT_READY` behavior until a genuinely tested, evidence-backed engine is integrated.
- Any changed file must be listed in the integration manifest and covered by tests.

## Baseline status
The repository foundation is present and its current backend tests/migrations pass in the uploaded
archive. The actual meter engine, verified rule corpus, complete live analysis, durable offline
storage, Android wrapper, APK build/release, and deployment verification remain unfinished.
