"""
Phase 10 — End-to-End Processing Pipeline
==========================================

run_pipeline(screenshot_id) executes the full processing chain for a
screenshot in the background, updating DB state at every stage.

Pipeline stages (sequential):
    PREPROCESSING → OCR → AI_EXTRACTION → EMBEDDING → RELATIONSHIPS

Design rules:
- Each stage is wrapped in its own ProcessingJob row (QUEUED → RUNNING → COMPLETED/FAILED).
- Screenshot.status mirrors the overall result (PROCESSING → COMPLETED or FAILED).
- Idempotent: re-running the same screenshot_id skips already-COMPLETED stages.
- No Celery/Redis — uses Python threading (caller's responsibility).
- run_pipeline() manages its own DB session so it is safe to call from a daemon thread.
"""

from __future__ import annotations

import logging
import uuid as uuid_mod
from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.memory import Memory
from app.models.processing_job import JobStage, JobStatus, ProcessingJob
from app.models.screenshot import Screenshot, ScreenshotStatus
from app.processing.ocr.provider import run_ocr
from app.processing.relationships import compute_relationships_for_memory

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_or_create_job(
    db: Session,
    screenshot_id: UUID,
    stage: JobStage,
) -> ProcessingJob:
    """
    Return the existing ProcessingJob for this screenshot+stage,
    or create a new QUEUED one.  Prevents duplicate job rows on retry.
    """
    existing = (
        db.query(ProcessingJob)
        .filter_by(screenshot_id=screenshot_id, stage=stage)
        .first()
    )
    if existing:
        return existing

    job = ProcessingJob(
        screenshot_id=screenshot_id,
        stage=stage,
        status=JobStatus.QUEUED,
    )
    db.add(job)
    db.flush()
    return job


def _run_stage(
    db: Session,
    job: ProcessingJob,
    fn: Callable[[], None],
) -> bool:
    """
    Execute *fn* inside a try/except, updating job status accordingly.
    Returns True on success, False on failure.
    """
    # Skip already-completed stages (idempotency)
    if job.status == JobStatus.COMPLETED:
        logger.info("Stage %s already COMPLETED — skipping.", job.stage)
        return True

    job.status = JobStatus.RUNNING
    job.started_at = _now()
    db.flush()

    try:
        fn()
        job.status = JobStatus.COMPLETED
        job.completed_at = _now()
        db.flush()
        logger.info("Stage %s COMPLETED.", job.stage)
        return True
    except Exception as exc:
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        job.completed_at = _now()
        db.flush()
        logger.error("Stage %s FAILED: %s", job.stage, exc)
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_pipeline(
    screenshot_id: UUID,
    db: Optional[Session] = None,
) -> None:
    """
    Execute the full processing pipeline for *screenshot_id*.

    If *db* is not provided the pipeline creates and owns its own session
    (required when called from a background thread).

    Args:
        screenshot_id: UUID of the Screenshot to process.
        db:            Optional SQLAlchemy session (inject for testing).
    """
    # ── Session management ────────────────────────────────────────────────
    _owns_session = db is None
    if _owns_session:
        from app.db.session import SessionLocal
        db = SessionLocal()

    try:
        _execute_pipeline(db, screenshot_id)
    finally:
        if _owns_session:
            db.close()


def _execute_pipeline(db: Session, screenshot_id: UUID) -> None:
    """Inner implementation — assumes caller manages the session lifecycle."""

    # ── 0. Load screenshot ────────────────────────────────────────────────
    screenshot: Optional[Screenshot] = db.get(Screenshot, screenshot_id)
    if not screenshot:
        logger.error("Pipeline: Screenshot %s not found — aborting.", screenshot_id)
        return

    logger.info("Pipeline START for screenshot %s", screenshot_id)
    screenshot.status = ScreenshotStatus.PROCESSING
    db.commit()

    # ── Pre-create all job rows so they are visible immediately ───────────
    jobs: dict[JobStage, ProcessingJob] = {}
    for stage in (
        JobStage.PREPROCESSING,
        JobStage.OCR,
        JobStage.AI_EXTRACTION,
        JobStage.EMBEDDING,
        JobStage.INDEXING,
    ):
        jobs[stage] = _get_or_create_job(db, screenshot_id, stage)
    db.commit()

    # Shared state passed between stages via a mutable dict
    ctx: dict = {}

    # ── Stage 1: PREPROCESSING ───────────────────────────────────────────
    def _preprocess():
        """Verify the file path recorded at ingest time exists on disk."""
        import os
        if screenshot.file_path and not os.path.exists(screenshot.file_path):
            # Non-fatal in dev/test — log a warning but don't crash
            logger.warning(
                "Preprocessing: file not found at %s (may be in test env)",
                screenshot.file_path,
            )
        ctx["image_path"] = screenshot.file_path or ""

    ok = _run_stage(db, jobs[JobStage.PREPROCESSING], _preprocess)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Stage 2: OCR ─────────────────────────────────────────────────────
    def _ocr():
        """Run OCR on the preprocessed image and store text in a Memory row."""
        image_path = ctx.get("image_path", "")
        ocr_result = run_ocr(image_path, screenshot_id=str(screenshot_id))

        if ocr_result.error:
            raise RuntimeError(f"OCR error: {ocr_result.error}")

        # Create (or update) the Memory row for this screenshot
        existing_memory: Optional[Memory] = (
            db.query(Memory)
            .filter_by(screenshot_id=screenshot_id)
            .first()
        )
        if existing_memory:
            existing_memory.raw_ocr_text = ocr_result.full_text
            memory = existing_memory
        else:
            memory = Memory(
                screenshot_id=screenshot_id,
                raw_ocr_text=ocr_result.full_text,
                title=screenshot.original_filename or "Untitled",
                tags=[],
                content_type="screenshot",
            )
            db.add(memory)

        db.flush()
        ctx["memory"] = memory
        ctx["ocr_text"] = ocr_result.full_text

    ok = _run_stage(db, jobs[JobStage.OCR], _ocr)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Stage 3: AI_EXTRACTION ───────────────────────────────────────────
    def _ai_extraction():
        """
        Stub: in production this calls an LLM/NER model to extract entities,
        update memory.title, memory.summary, and memory.tags.
        For Phase 10 we record that this stage ran without crashing.
        """
        memory: Optional[Memory] = ctx.get("memory")
        if memory:
            # Minimal stub: derive a title from the filename if still 'Untitled'
            if memory.title in (None, "Untitled", screenshot.original_filename):
                ocr_text: str = ctx.get("ocr_text", "")
                if ocr_text:
                    # Use first 80 chars of OCR text as a rough title stub
                    memory.title = ocr_text[:80].split("\n")[0].strip() or memory.title
            db.flush()

    ok = _run_stage(db, jobs[JobStage.AI_EXTRACTION], _ai_extraction)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Stage 4: EMBEDDING ───────────────────────────────────────────────
    def _embedding():
        """
        Stub: in production this computes a vector embedding via an embedding model.
        Writes a placeholder string to memory.embedding_placeholder.
        Phase 7 will replace this with real pgvector embeddings.
        """
        memory: Optional[Memory] = ctx.get("memory")
        if memory:
            ocr_text: str = ctx.get("ocr_text", "")
            # Store a human-readable token count as placeholder embedding info
            token_approx = len(ocr_text.split())
            memory.embedding_placeholder = (
                f"phase10_stub:tokens={token_approx}"
            )
            db.flush()

    ok = _run_stage(db, jobs[JobStage.EMBEDDING], _embedding)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Stage 5: INDEXING (Relationships) ────────────────────────────────
    def _relationships():
        """Compute and persist relationships between this memory and others."""
        memory: Optional[Memory] = ctx.get("memory")
        if memory:
            compute_relationships_for_memory(db, memory_id=memory.id)

    ok = _run_stage(db, jobs[JobStage.INDEXING], _relationships)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Done ──────────────────────────────────────────────────────────────
    screenshot.status = ScreenshotStatus.COMPLETED
    db.commit()
    logger.info("Pipeline COMPLETED for screenshot %s", screenshot_id)


def _fail_screenshot(db: Session, screenshot: Screenshot) -> None:
    """Mark the screenshot as FAILED and commit."""
    screenshot.status = ScreenshotStatus.FAILED
    db.commit()
    logger.error("Pipeline FAILED for screenshot %s", screenshot.id)
