import uuid, enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class JobStage(str, enum.Enum):
    INGESTION = "ingestion"
    PREPROCESSING = "preprocessing"
    OCR = "ocr"
    AI_EXTRACTION = "ai_extraction"
    EMBEDDING = "embedding"
    INDEXING = "indexing"


class JobStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    screenshot_id = Column(UUID(as_uuid=True), ForeignKey("screenshots.id", ondelete="CASCADE"), nullable=False, index=True)
    stage = Column(Enum(JobStage, name="job_stage"), nullable=False, index=True)
    status = Column(Enum(JobStatus, name="job_status"), nullable=False, default=JobStatus.QUEUED, index=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(String(8), nullable=True, default="0")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    screenshot = relationship("Screenshot", back_populates="processing_jobs")

    def __repr__(self):
        return f"<ProcessingJob stage={self.stage} status={self.status}>"
