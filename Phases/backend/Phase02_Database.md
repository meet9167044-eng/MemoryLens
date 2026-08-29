# Phase 2 - PostgreSQL + pgvector Database

## Objective
Set up the PostgreSQL database, Alembic migrations, and SQLAlchemy models.

## Why the phase exists
To establish the persistence layer for all future pipeline stages (Screenshots, Memories, Vectors).

## Prerequisites
- Phase 1 (Backend Foundation)

## Files/modules involved
- `backend/app/db/session.py`
- `backend/app/db/base.py`
- `backend/app/models/*.py`
- `backend/migrations/`

## Implementation tasks
1. Connect FastAPI to PostgreSQL using SQLAlchemy.
2. Initialize Alembic for migrations.
3. Enable the `pgvector` extension in the first migration.
4. Define core models: `User`, `Screenshot`, `Memory`, `ProcessingJob`.

## Data structures
- Normalized relational models with primary keys, foreign keys, and timestamps.

## APIs
- None.

## Database changes
- Create initial tables and indices.

## Testing requirements
- Database integration tests verifying CRUD operations.

## Acceptance criteria
- Alembic `upgrade head` runs successfully.
- Models can be queried using a SQLAlchemy session.

## Failure cases
- Handle database connection timeouts safely.

## What NOT to implement
- Do not implement Neo4j, Pinecone, or other external vector databases. Use PostgreSQL + pgvector exclusively.

## Completion requirements
- Code merged and DB integration tests passing.

## STATUS.md update instructions
- Mark Phase 2 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
