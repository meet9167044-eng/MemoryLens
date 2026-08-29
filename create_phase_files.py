import os

base_dir = r"c:\Users\EIILADMIN\MemoryLens\MemoryLens"
phases_dir = os.path.join(base_dir, "Phases", "backend")

os.makedirs(phases_dir, exist_ok=True)

phases_content = {
    "Phase01_Backend_Foundation.md": """# Phase 1 - Backend Foundation

## Objective
Establish the foundational structure of the FastAPI backend.

## Why the phase exists
To provide a clean, isolated backend architecture (API, Services, Core, DB, Tests) that won't interfere with the existing frontend.

## Prerequisites
None.

## Files/modules involved
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/api/v1/health.py`
- `backend/requirements.txt`

## Implementation tasks
1. Create the `backend/` folder structure.
2. Setup FastAPI application factory in `main.py`.
3. Configure `pydantic-settings` for environment variables.
4. Create a simple GET `/api/v1/health` endpoint.

## Data structures
- `Settings` class for environment configuration.

## APIs
- `GET /api/v1/health`

## Database changes
- None.

## Testing requirements
- `pytest` configuration and test for the health check endpoint.

## Acceptance criteria
- Application boots successfully via `uvicorn`.
- Health check returns 200 OK.
- CORS is configured to allow frontend communication.

## Failure cases
- If `.env` is misconfigured, the app should fail to start clearly.

## What NOT to implement
- Do not add database connections or real APIs yet.

## Completion requirements
- Code merged and tests passing.

## STATUS.md update instructions
- Mark Phase 1 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
""",

    "Phase02_Database.md": """# Phase 2 - PostgreSQL + pgvector Database

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
""",

    "Phase03_Ingestion.md": """# Phase 3 - Screenshot Ingestion + Storage

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
""",

    "Phase04_Preprocessing.md": """# Phase 4 - Image Preprocessing

## Objective
Build a modular image manipulation pipeline.

## Why the phase exists
Raw screenshots often need cropping, resizing, or normalization before ML models (OCR/Vision) can process them accurately.

## Prerequisites
- Phase 3 (Ingestion)

## Files/modules involved
- `backend/app/processing/preprocessing.py`

## Implementation tasks
1. Create functions to resize, normalize, and crop images using `Pillow` or `OpenCV`.
2. Save preprocessed assets alongside the original screenshot (do NOT overwrite).
3. Record references to these new assets in the database.

## Data structures
- `ProcessedAsset` DB Model

## APIs
- None directly.

## Database changes
- Update Memory/Screenshot with processed asset paths.

## Testing requirements
- Test resizing logic and format normalization.

## Acceptance criteria
- Original images remain untouched.
- Pipeline successfully generates a normalized image ready for OCR.

## Failure cases
- Image too large to process in memory.

## What NOT to implement
- Do not apply heavy ML denoising yet unless explicitly required.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 4 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
""",

    "Phase05_OCR.md": """# Phase 5 - OCR

## Objective
Extract text, bounding boxes, and confidence scores from preprocessed images.

## Why the phase exists
To make the text content of the screenshot searchable and understandable.

## Prerequisites
- Phase 4 (Preprocessing)

## Files/modules involved
- `backend/app/processing/ocr/provider.py`
- `backend/app/models/ocr.py`

## Implementation tasks
1. Integrate `PaddleOCR` (or a defined abstraction).
2. Process the image to extract full text and individual text blocks.
3. Save results to `ocr_results` and `ocr_blocks` tables.

## Data structures
- `OCRResult`, `OCRBlock` DB Models.

## APIs
- None directly.

## Database changes
- Create/insert into `ocr_results` and `ocr_blocks`.

## Testing requirements
- Unit tests mocking the OCR engine to verify DB storage.
- E2E test with a sample image containing "RuntimeError: CUDA...".

## Acceptance criteria
- Text, confidence, and coordinates (x1,y1,x2,y2) are accurately stored.

## Failure cases
- OCR engine fails to load or process the image.

## What NOT to implement
- Do not discard bounding box data. It is needed for UI overlays later.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 5 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
""",

    "Phase06_Extraction.md": """# Phase 6 - Visual Understanding + Metadata + Entity Extraction

## Objective
Understand the context of the image and extract structured tags, metadata, and canonical entities.

## Why the phase exists
OCR alone is unstructured. We need structured data (App Name, Entities, Tags) to power filtering and relationships.

## Prerequisites
- Phase 5 (OCR)

## Files/modules involved
- `backend/app/processing/extraction/`
- `backend/app/models/entity.py`
- `backend/app/models/tag.py`

## Implementation tasks
1. Implement a Visual Understanding abstraction to detect UI types (e.g., Code editor, Browser).
2. Extract metadata (content type, programming language).
3. Extract entities (e.g., CUDA, PyTorch) and canonicalize them (python == Python).
4. Extract tags.

## Data structures
- `Entity`, `Tag`, `MemoryEntity`, `MemoryTag` models.

## APIs
- None directly.

## Database changes
- Create entity and tag relationship tables.

## Testing requirements
- Test entity canonicalization (e.g., deduplication).

## Acceptance criteria
- A screenshot of VS Code with a Python error correctly yields "VS Code", "Python", and "error" tags.

## Failure cases
- Extraction yields zero entities. System should gracefully continue.

## What NOT to implement
- Do not implement complex Knowledge Graph (Neo4j) setups.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 6 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
""",

    "Phase07_Embeddings.md": """# Phase 7 - Multimodal Embeddings

## Objective
Convert text and images into vector representations for similarity search.

## Why the phase exists
Semantic search requires embeddings to find concepts by meaning rather than exact keywords.

## Prerequisites
- Phase 6 (Extraction)

## Files/modules involved
- `backend/app/processing/embeddings/`

## Implementation tasks
1. Create a `TextEmbeddingProvider` (e.g., Sentence Transformers).
2. Create an `ImageEmbeddingProvider` (e.g., SigLIP).
3. Construct a rich text document per Memory (Title + Summary + OCR + Tags) and embed it.
4. Store vectors in PostgreSQL using `pgvector`.

## Data structures
- Vector columns in the `embeddings` table.

## APIs
- None directly.

## Database changes
- Ensure `pgvector` HNSW indices are applied.

## Testing requirements
- Verify vector dimensions match the DB column.

## Acceptance criteria
- Text and image vectors are generated and stored successfully without crashing.

## Failure cases
- Model out of memory on CPU/GPU.

## What NOT to implement
- Do not use Pinecone/Milvus.

## Completion requirements
- Code merged, tests passing.

## STATUS.md update instructions
- Mark Phase 7 as complete `[x]` under BACKEND IMPLEMENTATION STATUS.
""",

    "Phase08_Search.md": """# Phase 8 - Semantic + Hybrid Search

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
""",

    "Phase09_Relationships.md": """# Phase 9 - Relationship Engine

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
""",

    "Phase10_Pipeline.md": """# Phase 10 - End-to-End Processing Pipeline

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
""",

    "Phase11_API.md": """# Phase 11 - API + Frontend Integration

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
""",

    "Phase12_Testing.md": """# Phase 12 - Testing + Evaluation + Optimization

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
"""
}

# Write the phase files
for filename, content in phases_content.items():
    full_path = os.path.join(phases_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Successfully generated {len(phases_content)} Phase markdown files in {phases_dir}.")