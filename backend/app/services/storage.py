"""
StorageProvider — abstraction for saving uploaded screenshot files to disk.

Phase A upgrade:
  - Files saved to DATASET_STORAGE_PATH/raw/YYYY/MM/ (structured dataset)
  - Auto-generates 400px WEBP thumbnail → DATASET_STORAGE_PATH/thumbnails/
  - Returns thumbnail_path alongside existing metadata
  - SHA-256 deduplication: callers can check file_hash before calling save()
"""
import hashlib
import io
import uuid
from datetime import datetime
from pathlib import Path

from PIL import Image

from app.config import settings


THUMBNAIL_SIZE = (400, 400)  # max dimensions (aspect-ratio preserved)


class StorageProvider:
    """Handles saving files to the structured dataset directory."""

    def __init__(self, base_dir: str = None):
        base = Path(base_dir or settings.DATASET_STORAGE_PATH)
        self.raw_dir = base / "raw"
        self.thumb_dir = base / "thumbnails"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.thumb_dir.mkdir(parents=True, exist_ok=True)

        # Keep a legacy upload_dir alias for backward compat
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    # ── Helpers ────────────────────────────────────────────────────────────

    def compute_hash(self, data: bytes) -> str:
        """SHA-256 hash of file bytes — used for deduplication."""
        return hashlib.sha256(data).hexdigest()

    def build_raw_filepath(self, original_filename: str, file_hash: str) -> Path:
        """
        Structured storage path:
          data/dataset/raw/YYYY/MM/<hash[:12]>_<uuid8>.<ext>
        """
        today = datetime.utcnow()
        date_dir = self.raw_dir / str(today.year) / f"{today.month:02d}"
        date_dir.mkdir(parents=True, exist_ok=True)

        ext = Path(original_filename).suffix.lower() or ".png"
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{file_hash[:12]}_{unique_id}{ext}"
        return date_dir / filename

    def _generate_thumbnail(self, data: bytes, stem: str) -> Path | None:
        """
        Create a 400px WEBP thumbnail.  Returns the path on success, None on failure.
        """
        try:
            img = Image.open(io.BytesIO(data)).convert("RGB")
            img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
            thumb_path = self.thumb_dir / f"{stem}_thumb.webp"
            img.save(thumb_path, "WEBP", quality=80)
            return thumb_path
        except Exception:
            return None

    # ── Public API ─────────────────────────────────────────────────────────

    def save(self, data: bytes, original_filename: str) -> dict:
        """
        Save image bytes to the dataset raw directory and generate a thumbnail.

        Returns:
            dict with keys:
                file_path, file_hash, file_size_bytes, thumbnail_path (may be None)
        """
        file_hash = self.compute_hash(data)
        filepath = self.build_raw_filepath(original_filename, file_hash)

        with open(filepath, "wb") as f:
            f.write(data)

        thumb_path = self._generate_thumbnail(data, filepath.stem)

        return {
            "file_path": str(filepath),
            "file_hash": file_hash,
            "file_size_bytes": len(data),
            "thumbnail_path": str(thumb_path) if thumb_path else None,
        }

    def delete(self, file_path: str) -> bool:
        """Deletes a file from disk. Returns True if deleted, False if not found."""
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False


# Singleton instance used across the app
storage = StorageProvider()
