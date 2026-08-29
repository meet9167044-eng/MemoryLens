# Phase 9 - Relationship Engine

## Objective
Calculate and store relationships between different Memories.

## Why the phase exists
To power the "Connections" and "Related Memories" UI features.

## Prerequisites
- Phase 8 (Search)

## Files/modules involved
- `backend/app/processing/relationships.py`
- `backend/app/api/v1/memories.py`

## Implementation tasks
1. Build an engine that compares a new Memory to existing ones based on shared entities, tags, and semantic similarity.
2. Generate relationship records with scores and explanations.
3. Expose a `GET /api/v1/memories/{id}/related` endpoint.

## Data structures
- `Relationship` DB model (source_id, target_id, type, score).

## APIs
- `GET /api/v1/memories/{id}/related`

## Database changes
- Create the `relationships` table.

## Testing requirements
- Test that identical tags produce a strong relationship score.

## Acceptance criteria
- `mem_1827` and `mem_1842` are correctly linked if they share the "CUDA" entity.

## Failure cases
- Prevent duplicate undirected relationship rows.

## What NOT to implement
- Do not overbuild graph logic. Keep relationships relational.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 9 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
