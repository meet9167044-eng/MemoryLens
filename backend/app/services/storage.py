"""
StorageProvider — abstraction for saving uploaded screenshot files to disk.
Phase 3: Local file system only.
Future phases can swap this for S3 or GCS without changing the API layer.
"""
import hashlib
import os
import uuid
from datetime import datetime
from pathlib import Path

from app.config import settings


class StorageProvider:
    """Handles saving files to the local uploads directory."""

    def __init__(self, upload_dir: str = None):
        self.upload_dir = Path(upload_dir or settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def compute_hash(self, data: bytes) -> str:
        """SHA-256 hash of file bytes — used for deduplication."""
        return hashlib.sha256(data).hexdigest()

    def build_filepath(self, original_filename: str, file_hash: str) -> Path:
        """
        Builds a structured storage path:
          uploads/YYYY/MM/DD/<hash>_<uuid>.<ext>
        This prevents collisions and organizes files by date.
        """
        today = datetime.utcnow()
        date_dir = self.upload_dir / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
        date_dir.mkdir(parents=True, exist_ok=True)

        ext = Path(original_filename).suffix.lower() or ".png"
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{file_hash[:12]}_{unique_id}{ext}"
        return date_dir / filename

    def save(self, data: bytes, original_filename: str) -> dict:
        """
        Saves file bytes to disk. Returns storage metadata.

        Returns:
            dict with keys: file_path, file_hash, file_size_bytes
        """
        file_hash = self.compute_hash(data)
        filepath = self.build_filepath(original_filename, file_hash)

        with open(filepath, "wb") as f:
            f.write(data)

        return {
            "file_path": str(filepath),
            "file_hash": file_hash,
            "file_size_bytes": len(data),
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
