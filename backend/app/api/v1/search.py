"""
GET /api/v1/search — Phase 8: Semantic + Hybrid Search endpoint.

Query parameters (all validated by FastAPI/Pydantic):
    q           — search query (required, non-empty)
    limit       — results per page (default 10, max 50)
    offset      — pagination offset (default 0)
    source_type — filter by source app type
    date_from   — ISO date lower bound
    date_to     — ISO date upper bound

Returns:
    SearchResponse with ranked, paginated SearchResult items.
    Raw embedding vectors are never returned (per Phase 8 spec).
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.search import SearchRequest, SearchResponse
from app.services.search import SearchService

router = APIRouter()


def _get_search_service() -> SearchService:
    """Dependency injection — swap for a DB-backed service in production."""
    return SearchService()


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Hybrid semantic + keyword search over Memories",
    description=(
        "Accepts a natural-language query string, embeds it, performs vector "
        "similarity search combined with keyword matching, applies optional "
        "metadata filters, and returns paginated ranked Memory results. "
        "Raw embedding vectors are never exposed."
    ),
    response_description="Paginated list of ranked Memory results.",
)
def search_memories(
    q: str = Query(
        ...,
        min_length=1,
        description="Natural-language search query (required, non-empty)",
        example="GPU memory error in Python",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results to return (1–50)",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination offset",
    ),
    source_type: Optional[Literal["desktop", "browser", "terminal", "document", "other"]] = Query(
        default=None,
        description="Filter results to a specific source type",
    ),
    date_from: Optional[str] = Query(
        default=None,
        description="ISO 8601 lower bound for memory timestamp (e.g. 2026-01-01)",
    ),
    date_to: Optional[str] = Query(
        default=None,
        description="ISO 8601 upper bound for memory timestamp (e.g. 2026-12-31)",
    ),
    service: SearchService = Depends(_get_search_service),
) -> SearchResponse:
    """
    Search memories using hybrid semantic + keyword ranking.
    """
    request = SearchRequest(
        q=q,
        limit=limit,
        offset=offset,
        source_type=source_type,
        date_from=date_from,
        date_to=date_to,
    )
    return service.search(request)
