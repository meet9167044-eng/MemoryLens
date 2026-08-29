"""
MemoryLens FastAPI application entry point.

Routers registered:
    GET  /api/v1/health              — health check
    POST /api/v1/ingest              — file upload + background pipeline
    GET  /api/v1/ingest/{id}         — pipeline status
    GET  /api/v1/memories            — list all memories
    GET  /api/v1/memories/{id}       — memory detail
    GET  /api/v1/search              — hybrid keyword + vector search (GET)
    POST /api/v1/search/hybrid       — hybrid search (POST body)
    GET  /api/v1/timeline            — chronological grouped feed
    GET  /api/v1/connections         — graph nodes + edges
    POST /api/v1/chat                — RAG conversational assistant
    GET  /api/v1/screenshots/{id}/image — serve raw image bytes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import health, search, memories, timeline
from app.api.v1.ingest import router as ingest_router
from app.api.v1.connections import router as connections_router
from app.api.v1.chat import router as chat_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="MemoryLens backend API — multimodal AI memory search.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow the Vite frontend to call the API during development
# ---------------------------------------------------------------------------
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(ingest_router, tags=["ingestion"])           # ingest router has its own /api/v1 prefix
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["search"])
app.include_router(memories.router, prefix=settings.API_V1_STR)
app.include_router(timeline.router, prefix=settings.API_V1_STR)
app.include_router(connections_router, prefix=settings.API_V1_STR, tags=["connections"])
app.include_router(chat_router, prefix=settings.API_V1_STR, tags=["chat"])
