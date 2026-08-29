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
"""

import sys
import json
from pathlib import Path
from typing import Optional

from app.models.ocr import BoundingBox, OCRBlock, OCRResult


def run_ocr(image_path: str, screenshot_id: Optional[str] = None) -> OCRResult:
    """
    Run PaddleOCR on a given image and return a structured OCRResult.

    Args:
        image_path: Path to the screenshot/image file.
        screenshot_id: Optional ID to tag the result (default: filename).

    Returns:
        OCRResult with full_text and individual blocks.
    """
    # Use filename as default ID if not provided
    if screenshot_id is None:
        screenshot_id = Path(image_path).stem

    try:
        # Lazy import — so if PaddleOCR is not installed, only this function fails,
        # not the whole app.
        from paddleocr import PaddleOCR

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

    except ImportError:
        return OCRResult(
            screenshot_id=screenshot_id,
            full_text="",
            blocks=[],
            error="PaddleOCR is not installed. Run: pip install paddleocr paddlepaddle",
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
