# Phase 3 - Screenshot Ingestion + Storage

## Objective
Create the API to receive screenshots and store them safely.

## Why the phase exists
To capture the raw evidence (digital activity) before any processing begins.

## Prerequisites
- Phase 2 (Database)

## Files/modules involved
- `backend/app/api/v1/ingest.py`
- `backend/app/services/storage.py`
- `backend/app/models/screenshot.py`

## Implementation tasks
1. Create a `StorageProvider` abstraction for local file saving.
2. Build `POST /api/v1/ingest` accepting `multipart/form-data`.
3. Validate MIME type, extension, and decodability.
4. Calculate a file hash for deduplication.
5. Store a `Screenshot` record in the database.

## Data structures
- `ScreenshotUploadSchema` (Pydantic)
- `Screenshot` (SQLAlchemy)

## APIs
- `POST /api/v1/ingest`

## Database changes
- Insert rows into `screenshots` table.

## Testing requirements
- Test with valid images, invalid files (PDFs/Text), and oversized files.

## Acceptance criteria
- Valid images are saved to the local disk and DB.
- Invalid images are rejected with a 400 status.
- API returns a PENDING memory ID.

## Failure cases
- File write permissions error.
- Corrupted image upload.

## What NOT to implement
- Do not run OCR or embeddings synchronously in this API.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 3 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
