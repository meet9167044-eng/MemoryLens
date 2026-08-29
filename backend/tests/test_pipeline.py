"""
Phase 10 — End-to-End Pipeline Tests
--------------------------------------
All tests use in-memory SQLite via a real SQLAlchemy session.
`run_ocr` is mocked so no PaddleOCR installation is required.

Test coverage:
    1. Pipeline creates all 5 ProcessingJob rows.
    2. Screenshot.status becomes COMPLETED after pipeline.
    3. A Memory row is created for the screenshot.
    4. memory.raw_ocr_text contains the mocked OCR output.
    5. All ProcessingJob rows end with status=COMPLETED.
    6. When run_ocr raises, Screenshot.status becomes FAILED.
    7. Running the pipeline twice doesn't create duplicate job rows.
"""

from __future__ import annotations

import os
import sys
import uuid
from unittest.mock import patch, MagicMock

import pytest

# Ensure backend/ is importable when run via pytest from the backend/ dir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Must set TESTING=1 before any app import so Memory uses JSON not JSONB
os.environ.setdefault("TESTING", "1")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.screenshot import Screenshot, ScreenshotStatus
from app.models.memory import Memory
from app.models.processing_job import ProcessingJob, JobStatus, JobStage
from app.models.ocr import OCRResult
from app.jobs.pipeline import run_pipeline


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db():
    """Fresh in-memory SQLite session for every test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def _make_screenshot(db) -> Screenshot:
    """Helper: create and persist a PENDING screenshot."""
    scr = Screenshot(
        id=uuid.uuid4(),
        file_path="/tmp/test_shot.png",
        original_filename="test_shot.png",
        status=ScreenshotStatus.PENDING,
    )
    db.add(scr)
    db.commit()
    return scr


def _mock_ocr_result(screenshot_id: str, text: str = "Hello CUDA world") -> OCRResult:
    return OCRResult(
        screenshot_id=screenshot_id,
        full_text=text,
        blocks=[],
        error=None,
    )


# ---------------------------------------------------------------------------
# Helper: run pipeline with mocked OCR
# ---------------------------------------------------------------------------

def _run_with_mock_ocr(db, screenshot_id, ocr_text="Hello CUDA world"):
    """Run the pipeline with a mocked run_ocr that returns a fixed OCR result."""
    mock_result = _mock_ocr_result(str(screenshot_id), text=ocr_text)
    with patch("app.jobs.pipeline.run_ocr", return_value=mock_result):
        run_pipeline(screenshot_id=screenshot_id, db=db)


# ---------------------------------------------------------------------------
# Test 1: All 5 ProcessingJob rows are created
# ---------------------------------------------------------------------------

class TestPipelineCreatesJobs:
    def test_pipeline_creates_all_five_processing_jobs(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)

        jobs = db.query(ProcessingJob).filter_by(screenshot_id=scr.id).all()
        stages_found = {j.stage for j in jobs}

        expected = {
            JobStage.PREPROCESSING,
            JobStage.OCR,
            JobStage.AI_EXTRACTION,
            JobStage.EMBEDDING,
            JobStage.INDEXING,
        }
        assert expected == stages_found, (
            f"Missing stages: {expected - stages_found}"
        )


# ---------------------------------------------------------------------------
# Test 2: Screenshot.status becomes COMPLETED
# ---------------------------------------------------------------------------

class TestScreenshotStatusCompleted:
    def test_screenshot_status_is_completed_after_pipeline(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)

        db.refresh(scr)
        assert scr.status == ScreenshotStatus.COMPLETED, (
            f"Expected COMPLETED, got {scr.status}"
        )


# ---------------------------------------------------------------------------
# Test 3: A Memory record is created
# ---------------------------------------------------------------------------

class TestMemoryRecordCreated:
    def test_pipeline_creates_memory_record(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)

        memories = db.query(Memory).filter_by(screenshot_id=scr.id).all()
        assert len(memories) == 1, (
            f"Expected 1 Memory record, found {len(memories)}"
        )


# ---------------------------------------------------------------------------
# Test 4: Memory contains OCR text
# ---------------------------------------------------------------------------

class TestMemoryHasOCRText:
    def test_memory_raw_ocr_text_is_populated(self, db):
        scr = _make_screenshot(db)
        expected_text = "RuntimeError: CUDA out of memory."
        _run_with_mock_ocr(db, scr.id, ocr_text=expected_text)

        memory = db.query(Memory).filter_by(screenshot_id=scr.id).first()
        assert memory is not None
        assert memory.raw_ocr_text == expected_text, (
            f"Expected OCR text '{expected_text}', got '{memory.raw_ocr_text}'"
        )


# ---------------------------------------------------------------------------
# Test 5: All jobs end with COMPLETED status
# ---------------------------------------------------------------------------

class TestAllJobsCompleted:
    def test_all_processing_jobs_are_completed(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)

        jobs = db.query(ProcessingJob).filter_by(screenshot_id=scr.id).all()
        assert jobs, "No ProcessingJob rows found"
        for job in jobs:
            assert job.status == JobStatus.COMPLETED, (
                f"Stage {job.stage} has status {job.status}, expected COMPLETED"
            )


# ---------------------------------------------------------------------------
# Test 6: OCR failure marks screenshot as FAILED
# ---------------------------------------------------------------------------

class TestOCRFailure:
    def test_ocr_error_marks_screenshot_failed(self, db):
        scr = _make_screenshot(db)

        # Return an OCRResult with an error field set
        bad_result = OCRResult(
            screenshot_id=str(scr.id),
            full_text="",
            blocks=[],
            error="PaddleOCR crashed",
        )
        with patch("app.jobs.pipeline.run_ocr", return_value=bad_result):
            run_pipeline(screenshot_id=scr.id, db=db)

        db.refresh(scr)
        assert scr.status == ScreenshotStatus.FAILED, (
            f"Expected FAILED status after OCR error, got {scr.status}"
        )

    def test_ocr_exception_marks_screenshot_failed(self, db):
        scr = _make_screenshot(db)

        with patch("app.jobs.pipeline.run_ocr", side_effect=RuntimeError("GPU OOM")):
            run_pipeline(screenshot_id=scr.id, db=db)

        db.refresh(scr)
        assert scr.status == ScreenshotStatus.FAILED

    def test_ocr_job_has_error_message_on_failure(self, db):
        scr = _make_screenshot(db)
        bad_result = OCRResult(
            screenshot_id=str(scr.id),
            full_text="",
            blocks=[],
            error="Device not found",
        )
        with patch("app.jobs.pipeline.run_ocr", return_value=bad_result):
            run_pipeline(screenshot_id=scr.id, db=db)

        ocr_job = (
            db.query(ProcessingJob)
            .filter_by(screenshot_id=scr.id, stage=JobStage.OCR)
            .first()
        )
        assert ocr_job is not None
        assert ocr_job.status == JobStatus.FAILED
        assert ocr_job.error_message is not None


# ---------------------------------------------------------------------------
# Test 7: Idempotency — running twice creates no duplicate job rows
# ---------------------------------------------------------------------------

class TestPipelineIdempotency:
    def test_running_pipeline_twice_no_duplicate_jobs(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)
        _run_with_mock_ocr(db, scr.id)   # second run

        jobs = db.query(ProcessingJob).filter_by(screenshot_id=scr.id).all()
        # Should be exactly 5 rows — one per stage, no duplicates
        assert len(jobs) == 5, (
            f"Expected 5 job rows after two runs, found {len(jobs)}"
        )

    def test_running_pipeline_twice_no_duplicate_memories(self, db):
        scr = _make_screenshot(db)
        _run_with_mock_ocr(db, scr.id)
        _run_with_mock_ocr(db, scr.id)

        memories = db.query(Memory).filter_by(screenshot_id=scr.id).all()
        assert len(memories) == 1, (
            f"Expected 1 Memory after two runs, found {len(memories)}"
        )
