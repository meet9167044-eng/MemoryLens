"""
GET  /api/v1/search        — Phase C: Hybrid DB-backed search (primary)
POST /api/v1/search/hybrid — Phase C: Same, body-based variant for richer payloads

Uses DBSearchService when Memory rows exist in the database.
Falls back to synthetic SearchService when no memories have been uploaded yet.
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.memory import Memory
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search import SearchService
from app.services.db_search import DBSearchService

router = APIRouter()


def _pick_service(db: Session) -> object:
    """
    Return DBSearchService if any Memory rows exist (real data),
    otherwise fall back to the synthetic in-memory SearchService.
    """
    count = db.query(Memory).count()
    if count > 0:
        return DBSearchService(db)
    return SearchService()


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Hybrid semantic + keyword search over Memories",
    description=(
        "Searches across uploaded memories using keyword matching and (when a "
        "Gemini API key is configured) vector cosine similarity. "
        "Falls back to synthetic demo data when no files have been uploaded yet."
    ),
)
def search_memories(
    q: str = Query(..., min_length=1, description="Search query", example="GPU error in Python"),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    source_type: Optional[Literal["desktop", "browser", "terminal", "document", "other"]] = Query(default=None),
    date_from: Optional[str] = Query(default=None, description="ISO 8601 lower bound"),
    date_to: Optional[str] = Query(default=None, description="ISO 8601 upper bound"),
    db: Session = Depends(get_db),
) -> SearchResponse:
    """Search memories using hybrid semantic + keyword ranking."""
    service = _pick_service(db)
    request = SearchRequest(q=q, limit=limit, offset=offset, source_type=source_type,
                             date_from=date_from, date_to=date_to)
    return service.search(request)


@router.post(
    "/search/hybrid",
    response_model=SearchResponse,
    summary="Hybrid search (body-based POST)",
    description="Same as GET /search but accepts query params in the request body for richer filter support.",
)
def search_hybrid(
    request: SearchRequest,
    db: Session = Depends(get_db),
) -> SearchResponse:
    """POST version of hybrid search — accepts SearchRequest body."""
    service = _pick_service(db)
    return service.search(request)
