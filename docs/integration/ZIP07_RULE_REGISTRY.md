# ZIP 07 — Rule Registry & Provenance Integration

## Purpose

ZIP 07 adds explicit provenance classification to stored rules and exposes a read-only verified registry. It does **not** implement Somali metrical scanning and does not make database rules executable by the meter engine.

## Rule classes

- `GAARRIYE_PRIMARY` — rules directly supported by Gaarriye primary-source evidence.
- `RESEARCHER_INTERPRETATION` — researchers' interpretations; never attributed to Gaarriye.
- `COMPATIBLE_OTHER_RULE` — other rules explicitly reviewed as compatible with the selected framework.
- `UNCLASSIFIED` — default for existing or newly created rules until a reviewer assigns a defensible class.

The three selectable classes correspond to the independent Note Live switches. `UNCLASSIFIED` is an administrative holding value and is never returned by the new registry endpoint.

## Database change

Migration `0003_rule_provenance_class.py` adds `rules.rule_class`, non-null with server default `UNCLASSIFIED`, and an index. Existing rows are preserved and are **not** auto-classified. Downgrade removes only the new column and index.

## API

`GET /api/v1/rules/registry`

Optional query parameters:
- `genre_id`
- `rule_class`: `GAARRIYE_PRIMARY`, `RESEARCHER_INTERPRETATION`, or `COMPATIBLE_OTHER_RULE`

Only rows with `status=VERIFIED` and an explicit class are returned. Response includes `engine_executable: false` to make clear that verified metadata is not executable scansion logic.

The older `GET /api/v1/rules/verified?genre_id=...` endpoint remains for backward compatibility. New integrations should use `/api/v1/rules/registry` when provenance separation is required.

## Safety boundary

A rule's `VERIFIED` database status means its evidence passed the existing review workflow. It does not prove that the rule has a complete deterministic implementation, validated phonological behavior, or regression coverage. No rule is sent to `analyze_poem()` by this ZIP. The engine therefore continues to return `UNVERIFIED` until a later package adds reviewed executable specifications and tests.

## Files

- `backend/app/models.py` — UPDATE
- `backend/app/rule_service.py` — UPDATE
- `backend/app/main.py` — UPDATE
- `backend/tests/test_rule_service.py` — UPDATE
- `backend/tests/test_api.py` — UPDATE
- `database/migrations/versions/0003_rule_provenance_class.py` — NEW
- `docs/integration/ZIP07_RULE_REGISTRY.md` — NEW
- `ZIP_INSTALL_GUIDE.md` — NEW

No frontend files, source records, rule content, or earlier migrations are replaced.
