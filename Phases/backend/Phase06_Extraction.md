# Phase 6 - Visual Understanding + Metadata + Entity Extraction

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
