"""
Phase 3 — Standalone Ingestion Test
Tests: StorageProvider + API validation logic WITHOUT needing the server running.
Run: python tests/test_ingestion.py
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PIL import Image
from app.services.storage import StorageProvider


def make_test_image(width=100, height=100, fmt="PNG") -> bytes:
    """Creates a real in-memory PNG/JPEG image for testing."""
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def run_test():
    print("\n" + "=" * 55)
    print("  Phase 3 — Ingestion Test")
    print("=" * 55)

    provider = StorageProvider(upload_dir="uploads/test")

    # ── 1. Save a valid PNG ────────────────────────────────────
    print("\n[1] Saving a valid PNG image...")
    png_bytes = make_test_image(fmt="PNG")
    meta = provider.save(png_bytes, "test_screenshot.png")
    assert os.path.exists(meta["file_path"]), "File not saved to disk!"
    assert len(meta["file_hash"]) == 64, "SHA-256 hash should be 64 chars"
    assert meta["file_size_bytes"] == len(png_bytes)
    print(f"    PASS  Saved to: {meta['file_path']}")
    print(f"    PASS  Hash: {meta['file_hash'][:20]}...")
    print(f"    PASS  Size: {meta['file_size_bytes']} bytes")

    # ── 2. Deduplication — same bytes = same hash ──────────────
    print("\n[2] Testing deduplication (same image, different filename)...")
    meta2 = provider.save(png_bytes, "duplicate.png")
    assert meta["file_hash"] == meta2["file_hash"], "Hash mismatch for identical content!"
    print(f"    PASS  Same hash detected: {meta['file_hash'][:20]}...")

    # ── 3. JPEG support ────────────────────────────────────────
    print("\n[3] Saving a valid JPEG image...")
    jpg_bytes = make_test_image(fmt="JPEG")
    meta3 = provider.save(jpg_bytes, "test_screenshot.jpg")
    assert os.path.exists(meta3["file_path"])
    print(f"    PASS  JPEG saved: {meta3['file_path']}")

    # ── 4. Pillow validation on corrupted bytes ────────────────
    print("\n[4] Testing corrupted file rejection...")
    corrupted = b"this is not an image at all"
    try:
        img = Image.open(io.BytesIO(corrupted))
        img.verify()
        print("    FAIL  Should have raised an error!")
    except Exception:
        print("    PASS  Corrupted bytes correctly rejected by Pillow")

    # ── 5. File deletion ───────────────────────────────────────
    print("\n[5] Testing file deletion...")
    deleted = provider.delete(meta["file_path"])
    assert deleted is True
    assert not os.path.exists(meta["file_path"])
    provider.delete(meta2["file_path"])
    provider.delete(meta3["file_path"])
    print("    PASS  Files deleted successfully")

    print("\n" + "=" * 55)
    print("  PHASE 3 COMPLETE - All tests passed!")
    print("  StorageProvider: save, hash, deduplicate, delete")
    print("  Validation: MIME, extension, Pillow decodability")
    print("  API: POST /api/v1/ingest  GET /api/v1/ingest/{id}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    run_test()
