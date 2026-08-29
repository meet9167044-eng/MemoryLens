"""
OCR Data Models (Pydantic)
--------------------------
Defines the data structures for OCR output.
These act as the agreed-upon data contract between Phase 5 (OCR)
and later phases (Entity Extraction, Embeddings, Search).
"""

from pydantic import BaseModel
from typing import List, Optional


class BoundingBox(BaseModel):
    """Top-left (x1, y1) to bottom-right (x2, y2) coordinates."""
    x1: float
    y1: float
    x2: float
    y2: float


class OCRBlock(BaseModel):
    """A single block of text detected in a screenshot."""
    text: str
    confidence: float
    bounding_box: BoundingBox


class OCRResult(BaseModel):
    """
    The complete OCR result for one screenshot.
    - full_text: all extracted text joined together (for embedding/search)
    - blocks: individual text blocks with position and confidence
    """
    screenshot_id: str
    full_text: str
    blocks: List[OCRBlock]
    error: Optional[str] = None
