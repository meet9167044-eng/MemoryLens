"""
OCR Provider (Phase 5)
-----------------------
Wraps PaddleOCR into a clean function that:
  1. Takes an image file path (from Phase 4 preprocessing output)
  2. Runs PaddleOCR on it
  3. Returns a structured OCRResult (defined in app/models/ocr.py)

This module is completely standalone — it does NOT need a database or
FastAPI to work. Phase 1 & 2 will plug this in later.

Usage (standalone test):
    python provider.py <image_path>

Mocking note for tests:
    PaddleOCR is stored at module level as `PaddleOCR = None`.
    Tests patch `app.processing.ocr.provider.PaddleOCR` to inject a mock.
    The function checks `PaddleOCR is None` to detect missing installation.
"""

import sys
import json
from pathlib import Path
from typing import Optional

from app.models.ocr import BoundingBox, OCRBlock, OCRResult

# PaddleOCR is declared at module level as None so tests can patch it.
# At import time, NO expensive paddleocr code runs.
# _LOAD_ATTEMPTED prevents the real import running when PaddleOCR is patched to None.
PaddleOCR = None  # type: ignore
_LOAD_ATTEMPTED = False


def _load_paddle():
    """Lazily import PaddleOCR and store it back on the module so it is patchable.
    Skips if already loaded or if PaddleOCR has been patched (not None) by a test.
    """
    global PaddleOCR, _LOAD_ATTEMPTED
    # Skip if already attempted, or if PaddleOCR was patched to a mock (not None)
    if _LOAD_ATTEMPTED or PaddleOCR is not None:
        return
    _LOAD_ATTEMPTED = True
    try:
        from paddleocr import PaddleOCR as _PaddleOCR
        PaddleOCR = _PaddleOCR
    except (ImportError, Exception):
        pass  # stays None — caller handles it


def run_ocr(image_path: str, screenshot_id: Optional[str] = None) -> OCRResult:
    """
    Run PaddleOCR on a given image and return a structured OCRResult.

    Args:
        image_path: Path to the screenshot/image file.
        screenshot_id: Optional ID to tag the result (default: filename stem).

    Returns:
        OCRResult with full_text and individual OCR blocks with bounding boxes.
    """
    # Use filename as default ID if not provided
    if screenshot_id is None:
        screenshot_id = Path(image_path).stem

    # Try to load PaddleOCR if not already loaded or mocked
    _load_paddle()

    # Check if PaddleOCR is available (real install or injected mock)
    if PaddleOCR is None:
        return OCRResult(
            screenshot_id=screenshot_id,
            full_text="",
            blocks=[],
            error="PaddleOCR is not installed. Run: pip install paddleocr paddlepaddle",
        )

    try:
        print(f"[OCR] Initializing PaddleOCR engine...")
        ocr_engine = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)

        print(f"[OCR] Processing image: {image_path}")
        raw_result = ocr_engine.ocr(image_path, cls=True)

        blocks: list[OCRBlock] = []

        # PaddleOCR returns List[List] — the outer list is per page/image
        if raw_result and raw_result[0]:
            for line in raw_result[0]:
                # line = [ [[x1,y1],[x2,y2],[x3,y3],[x4,y4]], ('text', confidence) ]
                box_points = line[0]
                text = line[1][0]
                confidence = float(line[1][1])

                x_coords = [pt[0] for pt in box_points]
                y_coords = [pt[1] for pt in box_points]

                bbox = BoundingBox(
                    x1=min(x_coords),
                    y1=min(y_coords),
                    x2=max(x_coords),
                    y2=max(y_coords),
                )

                blocks.append(OCRBlock(
                    text=text,
                    confidence=round(confidence, 4),
                    bounding_box=bbox,
                ))

        # Combine all text into one string for embedding/search
        full_text = " ".join(block.text for block in blocks)

        print(f"[OCR] Extracted {len(blocks)} text blocks.")
        return OCRResult(
            screenshot_id=screenshot_id,
            full_text=full_text,
            blocks=blocks,
        )

    except Exception as e:
        return OCRResult(
            screenshot_id=screenshot_id,
            full_text="",
            blocks=[],
            error=str(e),
        )


# ── Standalone test runner ─────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python provider.py <path_to_image>")
        sys.exit(1)

    result = run_ocr(image_path=sys.argv[1])
    print(json.dumps(result.model_dump(), indent=2))
