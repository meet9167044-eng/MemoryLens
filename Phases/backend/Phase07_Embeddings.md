# Phase 7 - Multimodal Embeddings

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
