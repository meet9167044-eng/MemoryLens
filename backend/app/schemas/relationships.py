"""
Phase 9 - Pydantic schemas for the Relationships API.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

from app.models.relationship import RelationshipType


class RelatedMemoryResponse(BaseModel):
    """A single related memory returned by GET /api/v1/memories/{id}/related."""
    memory_id:   str
    title:       Optional[str] = None
    score:       float
    rel_type:    RelationshipType
    explanation: Optional[str] = None
    # Enriched fields — populated by joining against the Memory table
    summary:     Optional[str] = None
    timestamp:   Optional[str] = None

    model_config = {"from_attributes": True}


class RelatedMemoriesResponse(BaseModel):
    """Full response envelope for the related-memories endpoint."""
    memory_id: str
    related:   list[RelatedMemoryResponse]
