# Gaarriye Frontend — ZIP 06 Integration

ZIP 06 updates the ZIP 04 frontend to use the three-switch API contract introduced in ZIP 05.

## Updated behavior

- Sends `analysis_modes.gaarriye`, `analysis_modes.researchers`, and `analysis_modes.compatible_other` independently.
- Does not send the legacy single `mode` field.
- Re-runs the API analysis when a switch changes and there is existing text plus a configured API URL.
- Shows each returned line's `status` and `explanation_code` in the Note Live line list.
- Invalidates an old response when the user edits the poem, preventing stale results from being displayed as current.
- Preserves local draft storage, save, TXT export, line navigation, and the existing visual design.

## Install / API configuration

Open `index.html` in Chrome for local UI use. To connect the backend, set the `content` value of the `meta[name="gaarriye-api"]` element in `index.html` to the actual backend base URL (no trailing slash). Do not use a placeholder URL.

## Honest capability boundary

The backend currently returns `UNVERIFIED` because verified executable meter rules have not yet been integrated. A returned line status is a processing/status record, not proof that the line's meter has been calculated. This frontend does not infer weights or approve rules.

## Tests

```bash
python -m pytest frontend/tests -q
node --check frontend/app.js
```
