# Phase 8 - Semantic + Hybrid Search

## Objective
Create the retrieval API for finding relevant Memories.

## Why the phase exists
To allow the frontend to query the processed dataset via natural language.

## Prerequisites
- Phase 7 (Embeddings)

## Files/modules involved
- `backend/app/api/v1/search.py`
- `backend/app/services/search.py`

## Implementation tasks
1. Accept a user query string.
2. Embed the query string.
3. Perform a vector similarity search in `pgvector`.
4. Combine with full-text keyword search and metadata filters.
5. Rank and return paginated results.

## Data structures
- `SearchRequest`, `SearchResult` Pydantic models.

## APIs
- `GET /api/v1/search`

## Database changes
- None.

## Testing requirements
- Test semantic recall (e.g., "GPU problem" finds "CUDA error").

## Acceptance criteria
- API returns ranked Memories matching the query.

## Failure cases
- Empty search queries.

## What NOT to implement
- Do not expose raw vector floats to the frontend.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 8 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
