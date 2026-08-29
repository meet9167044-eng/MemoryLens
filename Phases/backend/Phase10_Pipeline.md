# Phase 10 - End-to-End Processing Pipeline

## Objective
String all processing stages together asynchronously.

## Why the phase exists
Processing an image takes time. The API must respond instantly, while processing happens in the background.

## Prerequisites
- Phase 9 (Relationships)

## Files/modules involved
- `backend/app/jobs/pipeline.py`

## Implementation tasks
1. Implement a background job runner (Local/Simple).
2. Execute stages sequentially: Preprocessing -> OCR -> Extraction -> Embeddings -> Relationships.
3. Track processing status (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`).
4. Support safe retries for idempotency.

## Data structures
- `ProcessingJob` DB model.

## APIs
- None directly.

## Database changes
- Updates to Memory `status` column.

## Testing requirements
- E2E test simulating a full upload and waiting for `COMPLETED` status.

## Acceptance criteria
- A single screenshot upload automatically triggers the full pipeline without crashing the API thread.

## Failure cases
- If OCR fails, the Memory is marked `FAILED`, and the error is logged.

## What NOT to implement
- Do not introduce Celery/Redis yet unless absolutely necessary for performance.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 10 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
