"""
MemoryLens FastAPI application entry point.

Routers registered:
    GET /api/v1/health   — Phase 1: health check
    GET /api/v1/search   — Phase 8: semantic + hybrid search
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import health, search

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.8.0",
    description="MemoryLens backend API — semantic screenshot memory search.",
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
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["search"])
