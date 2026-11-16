
# Database and Migrations

This directory contains the database structure and
version-controlled schema migrations.

## Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations

## Planned Data Domains

1. Sources and source pages
2. Poetry genres
3. Gaarriye metrical rules
4. Rule versions and evidence
5. Phonetic readings
6. Metrical patterns
7. Poetry examples
8. Validation cases
9. Research claims
10. Review history and audit logs

## Data Integrity

- Every approved rule must have supporting evidence.
- Unverified rules must not run in strict analysis mode.
- Original source text must be preserved.
- Rule changes must be versioned.
- Research interpretations must remain separate
  from authoritative Gaarriye rules.

## Migration Policy

All database schema changes must use Alembic migrations.

No production database schema should be created
from unverified metrical assumptions.

# Database Migrations

This project uses Alembic to manage database schema changes.

## Run migrations

From the backend directory:

```bash
alembic upgrade head
