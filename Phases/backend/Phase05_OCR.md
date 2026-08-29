# Phase 5 - OCR

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
