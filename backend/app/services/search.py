"""
SearchService — Phase 8: Semantic + Hybrid Search.

Pipeline (per query):
    1. Embed the query text using the lightweight vocab-based embedder.
    2. Compute cosine similarity against each memory's text document.
    3. Compute keyword score (term-in-text matching over OCR / title / summary / tags).
    4. Apply metadata filters (source_type, date_from, date_to).
    5. Compute hybrid score = 0.6 × semantic + 0.4 × keyword.
    6. Rank by hybrid score (descending) and paginate.

Production swap:
    Replace _load_memories() + _build_memory_vector() with a DB query that
    fetches precomputed pgvector embeddings and scores using:
        ORDER BY embedding <=> query_vector
    The service interface (search method signature + return types) stays identical.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import List, Optional, Tuple

from app.core.embeddings import embed_text, cosine_similarity
from app.data.synthetic_memories import SYNTHETIC_MEMORIES
from app.schemas.search import (
    EntityResult,
    SearchRequest,
    SearchResponse,
    SearchResult,
    SourceResult,
)

# ---------------------------------------------------------------------------
# Weights for hybrid scoring
# ---------------------------------------------------------------------------
_SEMANTIC_WEIGHT = 0.6
_KEYWORD_WEIGHT = 0.4

# Minimum hybrid score to include a result (filters out entirely irrelevant)
_MIN_SCORE_THRESHOLD = 0.05


def _build_memory_document(memory: dict) -> str:
    """
    Concatenate all searchable text fields into a single document string.
    This is what gets embedded to represent the memory.
    """
    content = memory.get("content", {})
    parts = [
        content.get("title", ""),
        content.get("summary", ""),
        content.get("ocrText", ""),
        " ".join(memory.get("tags", [])),
        " ".join(e.get("name", "") for e in memory.get("entities", [])),
        memory.get("source", {}).get("app", ""),
    ]
    return " ".join(p for p in parts if p)


def _keyword_score(query: str, memory: dict) -> float:
    """
    Keyword relevance score: fraction of query terms found in the memory document.

    Returns a float in [0.0, 1.0].
    """
    document = _build_memory_document(memory).lower()
    query_terms = [t for t in re.split(r"[^a-z0-9]+", query.lower()) if t]
    if not query_terms:
        return 0.0

    hits = sum(1 for term in query_terms if term in document)
    return hits / len(query_terms)


def _semantic_score(query_vec: tuple, memory: dict) -> float:
    """
    Semantic relevance score via cosine similarity between query and memory vectors.

    Returns a float in [0.0, 1.0].
    """
    memory_doc = _build_memory_document(memory)
    memory_vec = embed_text(memory_doc)
    return cosine_similarity(query_vec, memory_vec)


def _hybrid_score(query_vec: tuple, query: str, memory: dict) -> Tuple[float, str]:
    """
    Combine semantic and keyword scores into a single hybrid score.

    Returns:
        (score, match_type) where match_type is 'semantic', 'keyword', or 'hybrid'.
    """
    sem = _semantic_score(query_vec, memory)
    kw = _keyword_score(query, memory)
    score = _SEMANTIC_WEIGHT * sem + _KEYWORD_WEIGHT * kw

    # Determine dominant match type for the result metadata
    if sem > 0.3 and kw > 0.3:
        match_type = "hybrid"
    elif sem >= kw:
        match_type = "semantic"
    else:
        match_type = "keyword"

    return round(score, 4), match_type


def _passes_filters(
    memory: dict,
    source_type: Optional[str],
    date_from: Optional[str],
    date_to: Optional[str],
) -> bool:
    """
    Apply metadata filters.  Returns False if the memory should be excluded.
    """
    # Source type filter
    if source_type is not None:
        if memory.get("source", {}).get("type") != source_type:
            return False

    # Date filters
    ts_str = memory.get("timestamp", "")
    if ts_str and (date_from or date_to):
        try:
            # Parse up to seconds — the synthetic data uses ISO format
            ts = datetime.fromisoformat(ts_str)
            if date_from:
                if ts < datetime.fromisoformat(date_from):
                    return False
            if date_to:
                if ts > datetime.fromisoformat(date_to):
                    return False
        except ValueError:
            # If timestamp is malformed, don't filter it out — fail open
            pass

    return True


def _make_snippet(query: str, memory: dict, max_chars: int = 200) -> str:
    """
    Return the first `max_chars` characters of OCR text, or an excerpt
    containing the first matched query term if possible.
    """
    ocr = memory.get("content", {}).get("ocrText", "")
    if not ocr:
        return memory.get("content", {}).get("summary", "")[:max_chars]

    # Try to find and surface the most relevant excerpt
    query_terms = [t for t in re.split(r"[^a-z0-9]+", query.lower()) if t]
    ocr_lower = ocr.lower()

    best_pos = len(ocr)
    for term in query_terms:
        pos = ocr_lower.find(term)
        if 0 <= pos < best_pos:
            best_pos = pos

    if best_pos < len(ocr):
        start = max(0, best_pos - 40)
        snippet = ocr[start : start + max_chars]
        if start > 0:
            snippet = "…" + snippet
        return snippet

    return ocr[:max_chars]


def _to_search_result(memory: dict, score: float, match_type: str, query: str) -> SearchResult:
    """Convert a raw synthetic memory dict into a SearchResult Pydantic model."""
    content = memory.get("content", {})
    source_raw = memory.get("source", {})
    entities_raw = memory.get("entities", [])

    return SearchResult(
        id=memory["id"],
        timestamp=memory["timestamp"],
        source=SourceResult(
            app=source_raw.get("app", "Unknown"),
            type=source_raw.get("type", "other"),
        ),
        title=content.get("title", "Untitled"),
        summary=content.get("summary", ""),
        ocr_snippet=_make_snippet(query, memory),
        tags=memory.get("tags", []),
        entities=[
            EntityResult(
                id=e.get("id", ""),
                name=e.get("name", ""),
                type=e.get("type", "other"),
            )
            for e in entities_raw
        ],
        image_url=memory.get("screenshot", {}).get("imageUrl", ""),
        relevance_score=score,
        match_type=match_type,  # type: ignore[arg-type]
    )


class SearchService:
    """
    Hybrid search over the synthetic memory store.

    Usage:
        service = SearchService()
        response = service.search(SearchRequest(q="GPU error"))
    """

    def __init__(self) -> None:
        # In production: accept a DB session / async client here
        self._memories = SYNTHETIC_MEMORIES

    def search(self, request: SearchRequest) -> SearchResponse:
        """
        Execute hybrid search and return a paginated SearchResponse.

        Steps:
            1. Embed query.
            2. Score every memory (semantic + keyword).
            3. Apply filters.
            4. Sort by hybrid score descending.
            5. Paginate with limit/offset.
        """
        query = request.q.strip()
        query_vec = embed_text(query)

        scored: List[Tuple[float, str, dict]] = []

        for memory in self._memories:
            # Metadata filter first (cheap)
            if not _passes_filters(
                memory, request.source_type, request.date_from, request.date_to
            ):
                continue

            score, match_type = _hybrid_score(query_vec, query, memory)

            if score >= _MIN_SCORE_THRESHOLD:
                scored.append((score, match_type, memory))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        # Total before pagination
        total = len(scored)

        # Paginate
        page = scored[request.offset : request.offset + request.limit]

        results = [
            _to_search_result(memory, score, match_type, query)
            for score, match_type, memory in page
        ]

        return SearchResponse(
            query=query,
            total=total,
            limit=request.limit,
            offset=request.offset,
            results=results,
        )
