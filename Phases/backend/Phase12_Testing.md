# Phase 12 - Testing + Evaluation + Optimization

## Objective
Evaluate search/relationship quality and optimize backend performance.

## Why the phase exists
To ensure the product actually works well with a realistic dataset (30-60 memories).

## Prerequisites
- Phase 11 (API)

## Files/modules involved
- `backend/scripts/seed.py`
- `backend/tests/eval/`

## Implementation tasks
1. Write a `seed.py` script to populate the DB with realistic DevJams/CUDA synthetic memories.
2. Evaluate Precision@K and Recall@K for standard search queries.
3. Optimize lazy-loading of heavy ML models (OCR/Embeddings) so they don't block memory unnecessarily.

## Data structures
- Seed JSON files.

## APIs
- None.

## Database changes
- None.

## Testing requirements
- Search Quality E2E tests.

## Acceptance criteria
- Searching "CUDA memory error" reliably returns `mem_1827` at Rank 1.
- Backend handles 100 seeded memories efficiently.

## Failure cases
- Search accuracy drops.

## What NOT to implement
- Do not over-optimize for millions of rows.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 12 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
