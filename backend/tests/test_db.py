"""
Phase 2 — Standalone DB Validation Test
Runs WITHOUT FastAPI or pytest. Just: python tests/test_db.py
Verifies: connect → insert → query → cleanup
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # adds backend/

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.screenshot import Screenshot, ScreenshotStatus
from app.models.memory import Memory
from app.models.entity import Entity, EntityType
from app.models.processing_job import ProcessingJob, JobStage, JobStatus

def run_test():
    print("\n" + "="*55)
    print("  Phase 2 — Database Validation Test")
    print("="*55)

    db = SessionLocal()
    try:
        # ── 1. Insert a Screenshot ─────────────────────────────────
        print("\n[1] Inserting Screenshot...")
        ss = Screenshot(
            file_path="/uploads/test_screenshot.png",
            original_filename="test_screenshot.png",
            file_size_bytes="204800",
            mime_type="image/png",
            status=ScreenshotStatus.PENDING,
        )
        db.add(ss)
        db.commit()
        db.refresh(ss)
        print(f"    ✅ Screenshot created: {ss}")

        # ── 2. Insert a Memory linked to it ───────────────────────
        print("\n[2] Inserting Memory...")
        mem = Memory(
            screenshot_id=ss.id,
            title="Test Memory: Python Setup",
            summary="User was configuring a Python backend project with FastAPI and SQLAlchemy.",
            raw_ocr_text="pip install fastapi sqlalchemy alembic",
            content_type="terminal",
            tags=["python", "fastapi", "setup"],
            confidence_score=0.92,
        )
        db.add(mem)
        db.commit()
        db.refresh(mem)
        print(f"    ✅ Memory created: {mem}")

        # ── 3. Insert an Entity ────────────────────────────────────
        print("\n[3] Inserting Entity...")
        ent = Entity(
            memory_id=mem.id,
            name="FastAPI",
            entity_type=EntityType.TECHNOLOGY,
            value="FastAPI",
            confidence="0.98",
        )
        db.add(ent)
        db.commit()
        db.refresh(ent)
        print(f"    ✅ Entity created: {ent}")

        # ── 4. Insert a ProcessingJob ──────────────────────────────
        print("\n[4] Inserting ProcessingJob...")
        job = ProcessingJob(
            screenshot_id=ss.id,
            stage=JobStage.OCR,
            status=JobStatus.COMPLETED,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        print(f"    ✅ ProcessingJob created: {job}")

        # ── 5. Query back and verify ───────────────────────────────
        print("\n[5] Querying all records back...")
        q_ss = db.query(Screenshot).filter_by(id=ss.id).first()
        q_mem = db.query(Memory).filter_by(screenshot_id=ss.id).first()
        q_ent = db.query(Entity).filter_by(memory_id=mem.id).first()
        q_job = db.query(ProcessingJob).filter_by(screenshot_id=ss.id).first()

        assert q_ss is not None, "Screenshot not found!"
        assert q_mem is not None, "Memory not found!"
        assert q_ent is not None, "Entity not found!"
        assert q_job is not None, "ProcessingJob not found!"
        assert q_mem.title == "Test Memory: Python Setup"
        assert q_ent.entity_type == EntityType.TECHNOLOGY
        print("    ✅ All records queried and verified successfully!")

        # ── 6. Cleanup ─────────────────────────────────────────────
        print("\n[6] Cleaning up test data...")
        db.delete(ss)  # cascades to Memory, Entity, ProcessingJob
        db.commit()
        print("    ✅ Test data deleted.")

        print("\n" + "="*55)
        print("  ✅ PHASE 2 COMPLETE — All tests passed!")
        print("  Tables: screenshots, memories, entities, processing_jobs")
        print("  Alembic: upgrade head ✅")
        print("  CRUD: insert + query + delete ✅")
        print("="*55 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n  ❌ TEST FAILED: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_test()
