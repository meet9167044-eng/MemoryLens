# Phase 11 - API + Frontend Integration

## Objective
Finalize all REST endpoints required by the React frontend.

## Why the phase exists
To replace the synthetic data in the frontend with real data from the backend.

## Prerequisites
- Phase 10 (Pipeline)

## Files/modules involved
- `backend/app/api/v1/memories.py`
- `backend/app/api/v1/timeline.py`

## Implementation tasks
1. Create `GET /api/v1/memories` and `GET /api/v1/memories/{id}`.
2. Create `GET /api/v1/timeline`.
3. Ensure response JSON exactly matches the structure expected by the frontend's synthetic types.

## Data structures
- Pydantic models mapping DB rows to Frontend JSON.

## APIs
- `GET /api/v1/memories`
- `GET /api/v1/timeline`

## Database changes
- None.

## Testing requirements
- Endpoint tests verifying JSON schema compliance.

## Acceptance criteria
- The frontend can switch its data source to the backend API without breaking the UI.

## Failure cases
- Pagination out of bounds.

## What NOT to implement
- Do not change the frontend React components. Adapt the backend response to fit the frontend.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 11 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
