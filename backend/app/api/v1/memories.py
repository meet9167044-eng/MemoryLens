"""
Phase 9 - Memories API Router
Exposes:
  GET  /api/v1/memories/{id}/related  — returns related memories
  POST /api/v1/memories/{id}/compute-relationships  — trigger relationship engine
"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.relationships import RelatedMemoriesResponse, RelatedMemoryResponse
from app.processing.relationships import compute_relationships_for_memory, get_related_memories

router = APIRouter(prefix="/memories", tags=["memories"])


@router.get("/{memory_id}/related", response_model=RelatedMemoriesResponse)
def related_memories(
    memory_id: UUID,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Return the top *limit* memories most related to *memory_id*.
    Relationships are scored by shared entities, shared tags, and
    (eventually) semantic similarity.
    """
    rows = get_related_memories(db, memory_id=memory_id, limit=limit)
    if rows is None:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")

    return RelatedMemoriesResponse(
        memory_id=str(memory_id),
        related=[RelatedMemoryResponse(**r) for r in rows],
    )


@router.post("/{memory_id}/compute-relationships", status_code=202)
def trigger_compute_relationships(
    memory_id: UUID,
    min_score: float = Query(default=0.1, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
):
    """
    Trigger the relationship engine for *memory_id*.
    Compares this memory against all others and persists relationship rows.
    Returns a summary of how many were created/updated.
    """
    try:
        rels = compute_relationships_for_memory(db, memory_id=memory_id, min_score=min_score)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "memory_id": str(memory_id),
        "relationships_computed": len(rels),
        "status": "ok",
    }
