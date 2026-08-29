# Phase 4 - Image Preprocessing

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
