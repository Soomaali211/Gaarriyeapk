# ZIP 03 — Meter Engine Foundation Integration

## Reuse of existing architecture
The existing backend already has:
- `app/phonology_service.py` for conservative orthographic/phonological inspection.
- `app/rule_service.py` for rule registry operations.
- `Rule`, `RuleEvidence`, `Source`, and `ResearchClaim` SQLAlchemy models.
- `POST /api/v1/analyze`, which intentionally returns `ENGINE_NOT_READY`.

ZIP 03 adds a separate package at `backend/app/meter_engine/`. It does not duplicate
`phonology_service.py` or `rule_service.py`, and it does not change `main.py`.

## What is implemented
- Independent mode selection for Gaarriye primary rules, researcher interpretations,
  and other compatible rules.
- A stable result contract with statuses `VERIFIED`, `NON_CONFORMING`, `AMBIGUOUS`,
  `UNVERIFIED`, and `INVALID_CONFIGURATION`.
- Preservation of original non-empty verse lines and line numbers.
- Fail-closed behavior: no executable verified rule set means `UNVERIFIED`.
- Unit tests for mode selection, line preservation, and no-fabricated-verdict behavior.

## What is not implemented
- No vowel-length or consonant-weight calculation.
- No syllable segmentation or metrical pattern matcher.
- No genre classifier.
- No database query adapter that activates rules.
- No `/api/v1/analyze` integration.
- No claim that a line is non-conforming or that a poem is invalid.

## Why the endpoint is not changed
The existing API contract explicitly protects users from invented analysis by returning
`ENGINE_NOT_READY`. Connecting this scaffold to the endpoint as if it were a working
scansion engine would misrepresent its capability. Keep that behavior until verified
rule records, executable interpretations, and positive/negative/ambiguous regression
tests have been reviewed.

## Next integration gate
Before implementation of real scansion:
1. Inspect original Gaarriye sources and diagrams.
2. Approve each rule with exact source/page/diagram evidence.
3. Separate primary Gaarriye rules from researcher interpretations and compatible rules.
4. Define a formal representation for each verified rule.
5. Add independently reviewed test verses and edge cases.
6. Implement phonological segmentation only where supported by evidence.
7. Connect selected rule classes to the engine and then to the API.
8. Update the frontend only after the API contract is tested.
