"""
Unit Tests for OCR Provider (Phase 5)
--------------------------------------
Tests are written to work WITHOUT PaddleOCR installed.
The OCR engine is mocked so we validate our data-structuring
logic, not PaddleOCR itself.
"""

import pytest
from unittest.mock import patch, MagicMock

# Adjust path so tests can find backend modules when run from the backend/ dir
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.processing.ocr.provider import run_ocr
from app.models.ocr import OCRResult, OCRBlock, BoundingBox


# Simulated raw output that PaddleOCR would return
MOCK_PADDLE_OUTPUT = [
    [
        # Each item: [bounding_box_points, (text, confidence)]
        [[[10, 20], [200, 20], [200, 40], [10, 40]], ("RuntimeError: CUDA out of memory.", 0.9921)],
        [[[10, 50], [300, 50], [300, 70], [10, 70]], ("Tried to allocate 2.00 GiB (GPU 0)", 0.9873)],
        [[[10, 80], [250, 80], [250, 100], [10, 100]], ("PyTorch version: 2.1.0", 0.9654)],
    ]
]


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_returns_correct_number_of_blocks(MockPaddleOCR):
    """OCR result should have the same number of blocks as PaddleOCR output lines."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("fake_image.png", screenshot_id="test_001")

    assert isinstance(result, OCRResult)
    assert len(result.blocks) == 3


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_extracts_correct_text(MockPaddleOCR):
    """Each block text should match the mock output."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("fake_image.png", screenshot_id="test_001")

    assert result.blocks[0].text == "RuntimeError: CUDA out of memory."
    assert result.blocks[1].text == "Tried to allocate 2.00 GiB (GPU 0)"
    assert result.blocks[2].text == "PyTorch version: 2.1.0"


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_extracts_correct_bounding_boxes(MockPaddleOCR):
    """Bounding boxes should be correctly converted from polygon points to x1,y1,x2,y2."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("fake_image.png", screenshot_id="test_001")

    first_block = result.blocks[0]
    assert first_block.bounding_box.x1 == 10
    assert first_block.bounding_box.y1 == 20
    assert first_block.bounding_box.x2 == 200
    assert first_block.bounding_box.y2 == 40


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_full_text_joins_blocks(MockPaddleOCR):
    """full_text should be all block texts joined by a space."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("fake_image.png", screenshot_id="test_001")

    expected = "RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB (GPU 0) PyTorch version: 2.1.0"
    assert result.full_text == expected


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_confidence_is_rounded(MockPaddleOCR):
    """Confidence scores should be rounded to 4 decimal places."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("fake_image.png", screenshot_id="test_001")

    for block in result.blocks:
        # Should have at most 4 decimal places
        assert len(str(block.confidence).split(".")[-1]) <= 4


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_uses_filename_as_default_id(MockPaddleOCR):
    """If no screenshot_id is given, it should use the image filename (without extension)."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = MOCK_PADDLE_OUTPUT
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("my_screenshot.png")

    assert result.screenshot_id == "my_screenshot"


@patch("app.processing.ocr.provider.PaddleOCR")
def test_ocr_empty_image_returns_empty_blocks(MockPaddleOCR):
    """If PaddleOCR finds nothing (empty/blank image), result should have 0 blocks and empty text."""
    mock_engine = MagicMock()
    mock_engine.ocr.return_value = [[]]   # empty result
    MockPaddleOCR.return_value = mock_engine

    result = run_ocr("blank.png", screenshot_id="blank_001")

    assert result.blocks == []
    assert result.full_text == ""
    assert result.error is None


def test_ocr_missing_paddleocr_returns_error():
    """If PaddleOCR is not installed, run_ocr should return an error message, not crash."""
    with patch.dict("sys.modules", {"paddleocr": None}):
        result = run_ocr("fake_image.png", screenshot_id="err_test")

    assert result.error is not None
    assert "PaddleOCR" in result.error
