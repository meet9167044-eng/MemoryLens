import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

import os

# Use standard JSON if running with SQLite in tests, otherwise JSONB for Postgres
JSON_VARIANT = JSON if os.environ.get("TESTING", "") == "1" else JSONB


# NOTE: embedding column is a Text placeholder.
# Phase 7 member will run: ALTER TABLE memories ADD COLUMN embedding vector(1536)
# after installing the pgvector server extension.
EMBEDDING_DIM = 1536


class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    screenshot_id = Column(UUID(as_uuid=True), ForeignKey("screenshots.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(512), nullable=True)
    summary = Column(Text, nullable=True)
    raw_ocr_text = Column(Text, nullable=True)
    content_type = Column(String(128), nullable=True)
    tags = Column(JSON_VARIANT, nullable=True, default=list)
    confidence_score = Column(Float, nullable=True)
    # TODO (Phase 7): Replace with Vector(EMBEDDING_DIM) after pgvector is installed
    embedding_placeholder = Column(Text, nullable=True, comment="Placeholder for pgvector embedding — Phase 7 will migrate this to vector(1536)")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    screenshot = relationship("Screenshot", back_populates="memories")
    entities = relationship("Entity", back_populates="memory", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Memory id={self.id} title={self.title!r}>"
