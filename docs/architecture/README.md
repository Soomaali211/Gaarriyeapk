
# Gaarriye Analyzer — System Architecture

## 1. Overview

The system analyzes Somali poetry using a deterministic
metrical engine reconstructed from Gaarriye's original
publications and verified scholarly evidence.

## 2. Main Components

### Frontend
- HTML, CSS and JavaScript
- Poetry input
- Meter analysis interface
- Analysis results
- Genre reference and learning sections
- Backend API integration

### Backend
- Python
- FastAPI
- Text normalization
- Phonetic analysis
- Vowel quantity analysis
- Metrical segmentation
- Gaarriye rule engine
- Result explanation

### Database
- PostgreSQL
- SQLAlchemy
- Alembic
- Source records
- Rules and rule versions
- Evidence and validation cases
- Analysis history

### AI Integration
- Research assistance
- Ambiguity explanation
- Scholarly comparison
- Human review support

AI must not invent, approve or override Gaarriye rules.

## 3. Analysis Pipeline

1. Receive original poem text.
2. Preserve the original input.
3. Normalize text without destroying source data.
4. Identify words and phonetic readings.
5. Analyze vowel quantity.
6. Identify phonetic ambiguities.
7. Segment metrical units.
8. Apply verified genre-specific rules.
9. Check structural conditions and exceptions.
10. Generate an evidence-based result.
11. Store the analysis and engine version.

## 4. Analysis Status

- VERIFIED
- NON_CONFORMING
- AMBIGUOUS
- UNVERIFIED

Non-conforming means the poem does not conform
to Gaarriye's model. It does not mean the poem
is invalid Somali poetry.

## 5. Strict Mode

Only approved and evidence-supported rules may
participate in strict analysis.

Unverified rules must remain disabled.

## 6. Data Integrity

- Preserve original poetry.
- Preserve phonetic readings separately.
- Version every approved rule.
- Record source pages and evidence.
- Maintain an audit trail.
- Never silently resolve conflicting evidence.

## 7. Deployment

Planned deployment components:

- Frontend hosting
- FastAPI application server
- PostgreSQL database
- Environment configuration
- Automated tests
- GitHub Actions CI

## 8. Current Development Status

This document defines the intended architecture.
It does not claim that every component has
already been implemented.
