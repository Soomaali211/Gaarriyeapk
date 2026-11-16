# ZIP 04 Integration — Frontend & Note Live

## Existing frontend retained
This package uses the HTML/CSS/JS frontend from the uploaded repository. It does not replace
the design or remove the genre and source reference pages.

## Confirmed baseline mismatch
The uploaded `app.js` referenced `editorGutter`, `selectedLine`, `saveBtn`, and `downloadBtn`,
but the uploaded `index.html` did not define those IDs. ZIP 04 adds the missing elements.

## API contract boundary
The uploaded FastAPI `AnalyzeRequest` accepts `text`, `genre`, and `mode`
(`gaarriye_strict` or `research_comparison`). It uses `extra="forbid"` and does not accept
`analysis_modes`. ZIP 04 removes that unsupported field from frontend requests.

Since the backend cannot encode all three independent switch combinations, the frontend
declines to submit unsupported combinations rather than silently merging or mislabeling them.

## Live behavior
The editor tracks line numbers, current cursor line, selected line navigation, character count,
draft autosave, explicit save, and TXT export. These are editing features, not meter analysis.
The result must remain `ENGINE_NOT_READY` until verified rules and a tested engine are connected.

## Next required integration
A backend API update must accept the three independent rule classes, validate them, preserve
their provenance in responses, and have tests for every switch combination. Only then should
the frontend submit all three mode values.
