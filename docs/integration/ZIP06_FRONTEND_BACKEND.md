# ZIP 06 — Frontend / Backend Full Contract Integration

## Depends on

- ZIP 04 — Frontend & Note Live
- ZIP 05 — Backend & Database Integration

## File manifest

| Path | Action | Purpose |
|---|---|---|
| `frontend/app.js` | UPDATE | Sends the three independent API fields, handles line-level response data, refreshes on switch changes, and invalidates stale responses |
| `frontend/README.md` | UPDATE | Documents the new contract and capability boundary |
| `frontend/tests/test_frontend_contract.py` | UPDATE | Static tests for the ZIP 05 API contract and Note Live behavior |
| `docs/integration/ZIP06_FRONTEND_BACKEND.md` | NEW | Integration record |
| `ZIP_INSTALL_GUIDE.md` | NEW | Android-friendly installation instructions |

`frontend/index.html` and `frontend/styles.css` are unchanged from ZIP 04. No backend files, database models, migrations, or research records are changed by ZIP 06.

## API request contract

```json
{
  "text": "Sadarka koowaad\nSadarka labaad",
  "genre": "jiifto",
  "analysis_modes": {
    "gaarriye": true,
    "researchers": false,
    "compatible_other": true
  }
}
```

The frontend translates its saved local keys (`research`, `compatible`) to the exact backend names (`researchers`, `compatible_other`). It sends no legacy `mode` field. Each switch remains independent.

## Response handling

The UI reads `status`, `enabled_rule_classes`, and `lines[]`. For each non-empty line it matches `line_number` and displays the returned `status` and `explanation_code`. Editing the poem invalidates the previous response; changing a switch triggers a fresh request when an API URL and poem text are available.

## Safety and limitations

- `UNVERIFIED` is displayed as such; it is not converted into a positive or negative meter verdict.
- `analysis_performed: false` remains authoritative.
- No scansion, mora/weight calculation, rule approval, or genre validation is added here.
- If the API is not configured, the frontend keeps the draft locally and does not pretend analysis happened.
- CORS and the actual deployed API URL must be verified in the user's hosting environment; this package does not claim a remote deployment was updated.

## Verification

Static frontend tests and JavaScript syntax checks are run on the package. A real browser-to-deployed-API integration test still requires the actual backend URL and a live deployment.
