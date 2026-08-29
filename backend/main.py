"""
MemoryLens Backend — FastAPI Application Entry Point
Phase 3: Ingestion API wired up and running.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.ingest import router as ingest_router

app = FastAPI(
    title="MemoryLens API",
    description="AI-powered screenshot memory system backend.",
    version="0.3.0",
)

# Allow frontend (React/Vite) to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(ingest_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "MemoryLens API", "phase": 3}
