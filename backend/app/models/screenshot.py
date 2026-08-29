import enum, uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ScreenshotStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_path = Column(String(1024), nullable=False)
    original_filename = Column(String(512), nullable=True)
    file_size_bytes = Column(String(32), nullable=True)
    mime_type = Column(String(64), nullable=True, default="image/png")
    status = Column(Enum(ScreenshotStatus, name="screenshot_status"), nullable=False, default=ScreenshotStatus.PENDING, index=True)
    captured_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    memories = relationship("Memory", back_populates="screenshot", cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="screenshot", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Screenshot id={self.id} status={self.status}>"
