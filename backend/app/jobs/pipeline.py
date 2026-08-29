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
from app.models.entity import Entity, EntityType
from app.models.memory import Memory
from app.models.processing_job import JobStage, JobStatus, ProcessingJob
from app.models.screenshot import Screenshot, ScreenshotStatus
from app.processing.ocr.provider import run_ocr
from app.processing.relationships import compute_relationships_for_memory
from app.services.llm_extractor import llm_extractor

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Embedding helper (Phase C) — calls Gemini text-embedding-004 when available
# ---------------------------------------------------------------------------

def _compute_embedding(text: str) -> Optional[list]:
    """Return a float list embedding for text, or None on failure."""
    try:
        from app.config import settings
        if not settings.GEMINI_API_KEY:
            return None
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        result = genai.embed_content(
            model=f"models/{settings.EMBEDDING_MODEL}",
            content=text,
            task_type="RETRIEVAL_DOCUMENT",
        )
        return result["embedding"]
    except Exception as exc:
        logger.warning("Embedding generation failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Entity type mapper
# ---------------------------------------------------------------------------

_ENTITY_TYPE_MAP = {
    "technology": EntityType.TECHNOLOGY,
    "framework": EntityType.TECHNOLOGY,
    "tool": EntityType.OTHER,
    "company": EntityType.ORGANIZATION,
    "organization": EntityType.ORGANIZATION,
    "person": EntityType.PERSON,
    "topic": EntityType.OTHER,
    "other": EntityType.OTHER,
}


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

    # ── Stage 3: AI_EXTRACTION — Multimodal LLM ─────────────────────────
    def _ai_extraction():
        """
        Phase B: Call LLMExtractor (Gemini / OpenAI / stub) on the image.
        Extracts title, summary, OCR text (better quality than PaddleOCR),
        typed entities, tags, source app, and confidence score.
        Stores everything into the Memory row and creates Entity rows.
        """
        memory: Optional[Memory] = ctx.get("memory")
        if not memory:
            return

        # Load image bytes for LLM
        image_path: str = ctx.get("image_path", "")
        image_bytes: Optional[bytes] = None
        if image_path:
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            except OSError as e:
                logger.warning("Could not read image for LLM extraction: %s", e)

        if image_bytes:
            result = llm_extractor.extract(
                image_bytes,
                filename=screenshot.original_filename or "upload.png",
            )
        else:
            # No image bytes — fall back to OCR text we already have
            from app.services.llm_extractor import _stub_result
            result = _stub_result(screenshot.original_filename or "upload.png")

        # Update Memory fields
        if result.title:
            memory.title = result.title
        if result.summary:
            memory.summary = result.summary
        # Prefer LLM OCR text over PaddleOCR if LLM produced richer output
        if result.ocr_text and len(result.ocr_text) > len(memory.raw_ocr_text or ""):
            memory.raw_ocr_text = result.ocr_text
        memory.content_type = result.source_type
        memory.confidence_score = result.confidence
        memory.tags = result.tags

        # Delete any stale entity rows and create fresh ones from LLM output
        for old_ent in list(memory.entities):
            db.delete(old_ent)
        db.flush()

        for ext_ent in result.entities:
            etype = _ENTITY_TYPE_MAP.get(ext_ent.type.lower(), EntityType.OTHER)
            db.add(Entity(
                memory_id=memory.id,
                name=ext_ent.name,
                entity_type=etype,
                confidence="high",
            ))

        # Store for embedding stage
        ctx["llm_result"] = result
        db.flush()

    ok = _run_stage(db, jobs[JobStage.AI_EXTRACTION], _ai_extraction)
    if not ok:
        _fail_screenshot(db, screenshot)
        return

    # ── Stage 4: EMBEDDING — Real Gemini text-embedding ─────────────────
    def _embedding():
        """
        Phase C: Compute a real vector embedding for the memory using
        Gemini text-embedding-004 (768-dim) or fallback zero-vector.
        Stored as JSON text in embedding_placeholder until pgvector migration.
        """
        import json as _json
        memory: Optional[Memory] = ctx.get("memory")
        if not memory:
            return

        llm_res = ctx.get("llm_result")
        if llm_res:
            # Build composite embedding text from LLM results
            tag_str = " ".join(llm_res.tags)
            ent_str = " ".join(e.name for e in llm_res.entities)
            embed_text = (
                f"{memory.title or ''} | {memory.summary or ''} | "
                f"Tags: {tag_str} | Entities: {ent_str} | "
                f"Text: {(memory.raw_ocr_text or '')[:500]}"
            )
        else:
            embed_text = f"{memory.title or ''} {memory.raw_ocr_text or ''}"

        vector = _compute_embedding(embed_text)
        if vector:
            # Store as JSON array string — pgvector migration will move this to vector column
            memory.embedding_placeholder = _json.dumps(vector)
        else:
            memory.embedding_placeholder = ""
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
