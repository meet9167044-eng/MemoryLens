# MemoryLens — Complete End-to-End Completion Plan

## Goal
Transform MemoryLens from a polished demo shell into the actual 8.5/10 product:
**"Search your entire life through screenshots, with a knowledge graph of relationships between people / projects / websites / dates."**

This plan covers every gap found by deep-reading the source code, prioritized by impact, with concrete file-level actions.

---

## Current Reality (Code-Level Audit)

### Fixes for Your Encountered Issues
Based on your feedback that tags/summaries were missing and timestamps were wrong, here is the diagnosis and solution:

1. **Why tags/summaries were missing:** The LLM extraction failed and fell back to a "stub" (which only saves the filename). This happened because your `.env` specifies `GROQ_VISION_MODEL=openai/gpt-oss-20b`, which is not a valid Groq vision model. We will change this to `llama-3.2-11b-vision-preview` (a real Groq vision model) or instruct you to use Gemini.
2. **Why timestamps were wrong:** The system currently uses `created_at` (upload time). We need to extract the original timestamp from the image's EXIF metadata (or filename) and save it to a new `captured_at` column in the database, and configure the UI to show `captured_at` instead of `created_at`.

These exact fixes have been folded into **Phase A** and **Phase B** below.

### What actually works today
| Piece | Status |
|---|---|
| Upload → async pipeline → DB | ✅ Working |
| Groq/Gemini/OpenAI LLM extractor | ✅ Working (Groq key configured) |
| Keyword search on real DB rows | ✅ Working via `db_search.py` |
| Relationship model schema | ✅ Good foundation |
| Shared-entity + shared-tag relationships | ✅ Computed on ingest |
| RAG chat | ✅ Working |
| Frontend UI (8 pages) | ✅ Professional |

### What is broken / placeholder
| Piece | Gap |
|---|---|
| `embedding_placeholder` (Text column) | Embeddings stored as JSON string, never used for real vector search |
| pgvector | In `requirements.txt`, **never migrated** — column comment says "Phase 7 will migrate" |
| `EMBEDDING_PROVIDER=local` in `.env` | No local embedder wired; pipeline calls Gemini only |
| `RelationshipType.SEMANTIC` | Defined in model, **never computed** in `relationships.py` |
| Temporal clustering | Zero code — no date-proximity linking |
| Project / Story nodes | No concept exists in data model |
| `app_detected` from LLM extractor | Extracted correctly, **never persisted** to Memory model |
| Search (real DB) | O(n) Python cosine — loads all memories into memory |
| Dead pages | `src/pages/Overview.tsx`, `Connections.tsx`, `Memories.tsx`, `Timeline.tsx`, `Insights.tsx` (old flat files) alongside folder versions |
| Dead backend | `backend/main.py` (ingest-only stub, not the real app) |
| Connections page | Card grid, not an interactive graph — react-force-graph never integrated |
| Folder watcher / bulk import | Missing entirely |
| Deduplication | SHA-256 computed in `storage.py` but never checked before ingest |
| O(n²) relationship computation | Loads ALL memories on every ingest — will break at scale |
| Background jobs | Raw daemon threads, no queue, no retry |
| Insights page | Real API exists (`insights.py`) but frontend may still show hardcoded stats |
| `DEVELOPER.md` | Missing — no "how to run this" guide |
| Tests | `~60 tests` but no integration test for the full pipeline |

---

## Open Questions

> [!IMPORTANT]
> **Q1 — Deployment target?** Railway/Fly (cloud) or local-only personal tool? This changes whether we need auth, Docker, and a cloud-compatible vector DB.

> [!IMPORTANT]
> **Q2 — Embeddings offline?** The `.env` says `EMBEDDING_PROVIDER=local` but there's no local embedder. Do you want SentenceTransformers (free, offline, needs ~400MB model download) or keep using the Groq API for embeddings too?

> [!IMPORTANT]
> **Q3 — Graph UI priority?** Full interactive force-directed graph (react-force-graph) or a simplified hierarchical tree first?

> [!IMPORTANT]
> **Q4 — Timeline for completion?** 1 week (hackathon), 1 month (portfolio), or ongoing (personal tool)? This affects which phases to prioritize.

---

## Proposed Changes

All phases are ordered by impact and dependency. Each phase is independently deployable.

---

### Phase A — Codebase Cleanup (2–3 days) `Priority: CRITICAL`

**Goal**: One honest codebase, zero split-brain, zero misleading state.

---

#### [MODIFY] `backend/.env`
Fix the invalid Groq models so AI extraction actually works instead of failing silently:
```env
# Change these lines to real Groq models
GROQ_CHAT_MODEL=llama-3.1-8b-instant
GROQ_VISION_MODEL=llama-3.2-11b-vision-preview
```

#### [DELETE] `backend/main.py`
The ingest-only stub. Real app is `backend/app/main.py`.

#### [DELETE] `src/pages/Overview.tsx`
Replaced by the `src/pages/Overview/` folder version with real data.

#### [DELETE] `src/pages/Connections.tsx`
Replaced by `src/pages/Connections/`.

#### [DELETE] `src/pages/Memories.tsx`
Replaced by `src/pages/Memories/`.

#### [DELETE] `src/pages/Timeline.tsx`
Replaced by `src/pages/Timeline/`.

#### [DELETE] `src/pages/Insights.tsx`
Replaced by `src/pages/Insights/`.

#### [NEW] `DEVELOPER.md` (root)
The honest "how to run MemoryLens locally":
```
1. cd backend && pip install -r requirements.txt
2. alembic upgrade head
3. uvicorn app.main:app --reload
4. cd .. && npm install && npm run dev
5. Open http://localhost:5173
```
Include env var table, common errors, and how to get a Groq API key.

#### [MODIFY] [`backend/app/api/v1/insights.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/api/v1/insights.py)
- Remove any hardcoded stats
- Add `ocr_confidence_avg` from real `confidence_score` column
- Add `processing_success_rate` from `ScreenshotStatus.COMPLETED / total`
- Add `app_breakdown` (count per `content_type`)

#### [MODIFY] [`STATUS.md`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/STATUS.md)
Rewrite to reflect honest current state.

#### [MODIFY] [`backend/app/services/storage.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/services/storage.py)
- Check `file_hash` against existing Screenshot rows before saving
- Return existing `screenshot_id` if duplicate detected
- Prevents re-processing identical screenshots

---

### Phase B — Persist `app_detected` + Fix Memory Model (1 day) `Priority: HIGH`

**Goal**: Every memory knows what app it came from. Immediate UX win.

#### [MODIFY] [`backend/app/models/memory.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/models/memory.py)
Add two new columns:
```python
app_detected = Column(String(256), nullable=True)   # "VS Code", "Chrome", "Terminal"
captured_at  = Column(DateTime(timezone=True), nullable=True)  # from EXIF or filename
```

#### [NEW] Alembic migration
`alembic revision --autogenerate -m "add_app_detected_captured_at"`

#### [MODIFY] [`backend/app/jobs/pipeline.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/jobs/pipeline.py)
In the preprocessing stage (`_preprocess()`), add logic to extract the date from EXIF data or filename patterns, and update the `captured_at` column on the screenshot model.

In the AI extraction stage (`_ai_extraction()`), add:
```python
memory.app_detected = result.app_detected  # was being discarded!
```

#### [MODIFY] [`backend/app/services/db_search.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/services/db_search.py)
- Replace `SourceResult(app="Unknown", ...)` with `SourceResult(app=memory.app_detected or "Unknown", ...)`

#### [MODIFY] Frontend memory cards
Show `app_detected` badge on search results, memory cards, and timeline entries.

---

### Phase C — Real Vector Search with pgvector (1 week) `Priority: HIGH`

**Goal**: "Find the CUDA error screenshot" works reliably at 5,000+ screenshots. O(log n) not O(n).

#### [MODIFY] [`backend/app/models/memory.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/models/memory.py)
```python
# Replace embedding_placeholder Text with real pgvector column
from pgvector.sqlalchemy import Vector
embedding = Column(Vector(768), nullable=True)   # 768-dim for text-embedding-004
# Keep embedding_placeholder for migration compatibility, mark deprecated
```

#### [NEW] Alembic migration
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
-- Add embedding column
ALTER TABLE memories ADD COLUMN embedding vector(768);
-- Add HNSW index for fast ANN search
CREATE INDEX memories_embedding_hnsw_idx 
  ON memories USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

#### [MODIFY] [`backend/app/jobs/pipeline.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/jobs/pipeline.py)
`_embedding()` stage: store vector in `memory.embedding` (pgvector column), not `embedding_placeholder`.

#### [NEW] `backend/app/core/local_embedder.py`
```python
# SentenceTransformers local embedder — no API key required
from sentence_transformers import SentenceTransformer
_model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, ~80MB
def embed_local(text: str) -> list[float]: ...
```

#### [MODIFY] `backend/app/config.py` + `_compute_embedding()` in pipeline
Embedding priority chain:
1. `EMBEDDING_PROVIDER=local` → SentenceTransformers (offline)
2. `EMBEDDING_PROVIDER=gemini` → Gemini text-embedding-004
3. `EMBEDDING_PROVIDER=groq` → Groq embedding endpoint
4. Fallback: zero vector (graceful degradation)

#### [MODIFY] [`backend/app/services/db_search.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/services/db_search.py)
Replace O(n) Python loop with pgvector operator:
```sql
SELECT *, embedding <=> :query_vec AS distance
FROM memories
WHERE embedding IS NOT NULL
ORDER BY embedding <=> :query_vec
LIMIT :limit
```
Hybrid score = 0.6 × pgvector cosine + 0.4 × PostgreSQL full-text (ts_rank).

#### [MODIFY] `backend/requirements.txt`
Add:
```
sentence-transformers>=2.7.0
fastembed>=0.2.0   # faster alternative
```

---

### Phase D — The Differentiator: Knowledge Graph Engine (2 weeks) `Priority: CRITICAL`

**Goal**: "Show everything related to my internship application from January."  
This is the 8.5/10 feature. Currently a 2/10.

#### D1 — Semantic Relationships (complete `RelationshipType.SEMANTIC`)

#### [MODIFY] [`backend/app/processing/relationships.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/processing/relationships.py)
Add `_score_semantic()`:
```python
def _score_semantic(memory_a: Memory, memory_b: Memory) -> tuple[float, str]:
    if memory_a.embedding is None or memory_b.embedding is None:
        return 0.0, ""
    # pgvector cosine similarity in Python (for batch processing)
    sim = 1.0 - cosine_distance(memory_a.embedding, memory_b.embedding)
    if sim < 0.65:
        return 0.0, ""
    return round(sim, 4), f"Semantic similarity: {sim:.0%}"
```
Call this in `compute_relationships_for_memory()` for `RelationshipType.SEMANTIC`.

#### D2 — Temporal Clustering

#### [MODIFY] [`backend/app/processing/relationships.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/processing/relationships.py)
Add `RelationshipType.TEMPORAL` to the model and a new scoring function:
```python
def _score_temporal(memory_a: Memory, memory_b: Memory) -> tuple[float, str]:
    """Screenshots taken within 2 hours of each other are temporally related."""
    if not memory_a.captured_at or not memory_b.captured_at:
        return 0.0, ""
    delta = abs((memory_a.captured_at - memory_b.captured_at).total_seconds())
    if delta > 7200:  # 2 hours
        return 0.0, ""
    score = 1.0 - (delta / 7200)
    return round(score, 4), f"Captured {int(delta/60)} minutes apart"
```

#### D3 — First-Class Graph Nodes (Projects, People, Domains)

#### [NEW] `backend/app/models/project.py`
```python
class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID, primary_key=True, ...)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    color = Column(String(16), nullable=True)   # for graph UI
    created_at = ...
    memories = relationship("MemoryProject", back_populates="project")
```

#### [NEW] `backend/app/models/memory_project.py`
Association table: `memory_id ↔ project_id` with a `confidence` float.

#### [NEW] `backend/app/services/project_detector.py`
Auto-detect projects from entity clusters:
```python
def detect_project(entities: list[str], tags: list[str]) -> str | None:
    """
    Heuristic: if a memory mentions "LinkedIn" + "resume" + "internship" 
    → auto-assign to "Job Search" project.
    Later: use clustering on entity co-occurrence.
    """
```

#### D4 — URL/Domain Linking

#### [MODIFY] [`backend/app/services/llm_extractor.py`](file:///c:/Users/MEET%20JAIN/OneDrive/Desktop/MemoryLens/backend/app/services/llm_extractor.py)
Extend the prompt to extract `url_detected` and `domain`:
```json
"url_detected": "<full URL visible in address bar if any>",
"domain": "<base domain e.g. github.com, stackoverflow.com>"
```

#### [MODIFY] [`backend/app/models/memory.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/models/memory.py)
Add `domain = Column(String(256), nullable=True)`.

#### [NEW] Domain-based relationship in relationships.py
```python
def _score_domain(memory_a: Memory, memory_b: Memory) -> tuple[float, str]:
    if not memory_a.domain or not memory_b.domain:
        return 0.0, ""
    if memory_a.domain == memory_b.domain:
        return 0.7, f"Same domain: {memory_a.domain}"
    return 0.0, ""
```

#### D5 — Story/Topic Grouping (Collections)

#### [NEW] `backend/app/services/story_builder.py`
Cluster memories into "stories" using:
1. Temporal proximity (within 24h window)
2. Shared entities (>= 2 shared)
3. Semantic similarity (>= 0.7)

```python
def build_stories(db: Session) -> list[Story]:
    """Group memories into named narrative collections."""
    ...
```

#### [NEW] `backend/app/models/story.py`
```python
class Story(Base):
    __tablename__ = "stories"
    id = Column(UUID, primary_key=True, ...)
    title = Column(String(256))          # auto-generated or user-set
    date_start = Column(DateTime, ...)
    date_end = Column(DateTime, ...)
    memory_ids = Column(JSONB)           # list of UUIDs
    entity_summary = Column(JSONB)       # top entities in this story
```

#### D6 — Interactive Graph UI

#### [MODIFY] `package.json`
Add `"react-force-graph": "^1.44.0"` (or `"@react-sigma/core"` for sigma.js).

#### [MODIFY] `src/pages/Connections/` components
Replace the card grid with `<ForceGraph2D>`:
- **Memory nodes**: colored by `content_type` (browser=blue, terminal=green, code=purple)
- **Entity nodes**: colored by `entity_type`
- **Project nodes**: large hub nodes with project color
- **Story nodes**: temporal clusters shown as bounding boxes
- **Edge thickness**: proportional to relationship `score`
- **Edge color**: by `rel_type` (semantic=purple, temporal=orange, domain=teal, entity=gray)
- **Click to focus**: clicking a node highlights its neighborhood (1-hop)
- **Search in graph**: filter nodes by entity/project name
- **Timeline slider**: filter graph to a date range

---

### Phase E — "Search Your Entire Life": Auto-Ingestion (1 week) `Priority: MEDIUM`

**Goal**: Not manual upload — automatic capture of new screenshots.

#### [NEW] `backend/app/services/folder_watcher.py`
```python
import watchdog
# Watch ~/Pictures/Screenshots (macOS/Linux) 
# or %USERPROFILE%\Pictures\Screenshots (Windows)
# On new .png/.jpg file: call ingest API
```

#### [MODIFY] `backend/app/api/v1/ingest.py`
Add bulk import endpoint:
```
POST /api/v1/ingest/bulk
Body: { folder_path: string }
```
Scans folder recursively, deduplicates by hash, queues all new files.

#### [MODIFY] `backend/app/jobs/pipeline.py` Stage 1 (PREPROCESSING)
Extract `captured_at` from:
1. EXIF `DateTimeOriginal` (Pillow)
2. Filename patterns: `Screenshot_2024-01-15_14-30.png`
3. File `mtime` as last resort

#### [NEW] `backend/app/api/v1/watch.py`
```
POST /api/v1/watch/start   → start folder watcher daemon
POST /api/v1/watch/stop    → stop watcher
GET  /api/v1/watch/status  → { active, watched_path, last_event }
```

#### [MODIFY] Frontend Settings page
Add "Auto-capture" toggle with watched folder path configuration.

---

### Phase F — Scalability & Robustness (1 week) `Priority: MEDIUM`

**Goal**: Works with 10,000+ screenshots without breaking.

#### F1 — Replace daemon threads with proper queue

#### [NEW] `backend/app/jobs/queue.py`
Simple in-process queue using `asyncio.Queue` (no Redis needed):
```python
class PipelineQueue:
    def __init__(self, workers: int = 3): ...
    async def enqueue(self, screenshot_id: UUID): ...
    async def _worker(self): ...
```

Alternatively: add `dramatiq` + Redis for production-grade retry.

#### F2 — Fix O(n²) relationship computation

#### [MODIFY] [`backend/app/processing/relationships.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/processing/relationships.py)
Don't compare against ALL memories. Use candidate selection:
1. Fetch candidates sharing at least one entity name (fast SQL query)
2. Fetch temporally-nearby memories (date range query)
3. Fetch semantic ANN candidates (pgvector top-K)
4. Only compare against this union (~50 candidates max, not 10,000)

```python
def _get_candidates(db: Session, memory: Memory, k: int = 50) -> list[Memory]:
    # Entity overlap candidates
    entity_names = [e.name.lower() for e in memory.entities]
    entity_candidates = (
        db.query(Memory)
        .join(Entity)
        .filter(func.lower(Entity.name).in_(entity_names))
        .filter(Memory.id != memory.id)
        .limit(k)
        .all()
    )
    # Temporal candidates (±24h)
    # ANN vector candidates
    return deduplicate(entity_candidates + temporal + ann)
```

#### F3 — Add deduplication at ingest

#### [MODIFY] [`backend/app/api/v1/ingest.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/api/v1/ingest.py)
Before creating a Screenshot row, check:
```python
existing = db.query(Screenshot).filter_by(file_hash=storage_meta["file_hash"]).first()
if existing:
    return ScreenshotUploadResponse(..., message="Duplicate — already ingested", ...)
```

#### F4 — Add content-hash to Screenshot model

#### [MODIFY] [`backend/app/models/screenshot.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/models/screenshot.py)
```python
file_hash = Column(String(64), nullable=True, index=True, unique=True)
```

---

### Phase G — UX Polish & Missing Features (3–5 days) `Priority: MEDIUM`

#### G1 — Natural Language Query Enhancement

#### [MODIFY] [`backend/app/api/v1/search.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/api/v1/search.py)
Pre-process query through LLM to extract intent:
```python
# "Show everything from my internship in January"
# → entities: ["internship"], date_from: "2024-01-01", date_to: "2024-01-31"
def parse_query_intent(q: str) -> SearchRequest: ...
```

#### G2 — Memory Detail Page: "Related Screenshots" panel

#### [MODIFY] `src/pages/MemoryDetail.tsx`
Use `GET /api/v1/memories/{id}/related` to show a sidebar of related screenshots with:
- Relationship type badge (semantic / temporal / domain / entity)
- Relationship score bar
- Quick preview thumbnail

#### G3 — Timeline: Real temporal visualization

#### [MODIFY] `src/pages/Timeline/`
- Group memories by day/week/month
- Show `captured_at` (not `created_at`) as the primary timestamp
- Add calendar heatmap showing activity density (like GitHub contributions)
- Click a day to filter memories to that day

#### G4 — Chat: Context-aware follow-up queries

#### [MODIFY] [`backend/app/api/v1/chat.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/api/v1/chat.py)
- Maintain conversation history in session
- When user asks "show me more like that last one", use the previous search result IDs as seeds for similarity search

#### G5 — Search: Faceted filters UI

#### [MODIFY] `src/pages/Search.tsx` or `src/pages/Search/`
Add sidebar with clickable facets:
- App (VS Code, Chrome, Terminal...)
- Content type (browser, desktop, document...)
- Date range picker
- Top entities
- Top tags (tag cloud)

---

### Phase H — Portfolio / Demo Preparation (3–5 days) `Priority: MEDIUM`

#### H1 — Seed realistic demo dataset

#### [NEW] `scripts/seed_demo.py`
Create 50 realistic fake screenshots covering:
- Python error debugging (CUDA, PyTorch)
- LinkedIn / internship application emails
- GitHub code review
- Stack Overflow research
- VS Code coding session
- Google Calendar meeting notes

This makes demos work even without real user data.

#### H2 — Demo walkthrough recording script

#### [NEW] `scripts/demo_flow.md`
Step-by-step demo script:
1. Upload 5 screenshots (CUDA error, internship email, LinkedIn, GitHub, terminal)
2. Search: "CUDA error" → shows the error screenshot
3. Search: "internship" → shows LinkedIn + email screenshots
4. Connections page → graph shows all screenshots linked through "Python" and "internship" entities
5. Chat: "What was I doing with CUDA?" → RAG answer with citation

#### H3 — README overhaul

#### [MODIFY] `README.md`
Replace 803-line vision doc with:
- 2-3 sentence pitch
- Animated GIF or screenshot carousel (4 images: search, graph, chat, timeline)
- "Quick Start" (5 commands)
- "How it works" (diagram)
- Tech stack table
- License

---

### Phase I — Additional Improvements Found in Code Review

#### I1 — OCR: Re-enable PaddleOCR as local path

#### [MODIFY] `backend/requirements.txt`
```
# Uncomment for local OCR (no API key needed):
# paddleocr>=2.7.0
# paddlepaddle>=2.6.0
```

#### [MODIFY] `backend/app/processing/ocr/provider.py`
Implement three-tier OCR fallback:
1. PaddleOCR (local, best quality for screenshots)
2. Gemini/Groq vision (already in LLM extractor — avoid duplicate)
3. Stub (empty string)

#### I2 — Entity normalization

#### [NEW] `backend/app/services/entity_normalizer.py`
Prevent duplicate entities like "VS Code", "vscode", "Visual Studio Code":
```python
ENTITY_ALIASES = {
    "vscode": "VS Code",
    "visual studio code": "VS Code",
    "python3": "Python",
    "pytorch": "PyTorch",
    ...
}
def normalize(name: str) -> str: ...
```

#### I3 — Add `captured_at` to OCR stage

Already mentioned in Phase B — extract from EXIF in preprocessing stage.

#### I4 — Rate limiting on the ingest endpoint

#### [MODIFY] [`backend/app/api/v1/ingest.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/api/v1/ingest.py)
Add `slowapi` rate limiter: `10 uploads per minute per IP` to prevent abuse.

#### I5 — Fix `file_size_bytes` column type

#### [MODIFY] [`backend/app/models/screenshot.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/models/screenshot.py)
Change `file_size_bytes = Column(String(32), ...)` → `Column(Integer, ...)`.
It is stored as a string in the ingest handler — fix both.

#### I6 — Add `app_detected` filter to search

#### [MODIFY] [`backend/app/services/db_search.py`](file:///c:/Users/MEET JAIN/OneDrive/Desktop/MemoryLens/backend/app/services/db_search.py)
Support `?app=VS Code` query param → `filter(Memory.app_detected == app)`.

#### I7 — ProcessingJob visibility in frontend

#### [MODIFY] Upload modal in frontend
Poll `GET /api/v1/ingest/{screenshot_id}` every 2s after upload.
Show individual stage progress: `Preprocessing → OCR → AI → Embedding → Indexing`
Currently the modal shows a spinner but not which stage is running.

---

## Priority Order (If You Only Have 2 Weeks)

| Week | Phases | Outcome |
|---|---|---|
| Week 1, Days 1–2 | Phase A (cleanup) + Phase B (app_detected) | Honest codebase, real app names shown |
| Week 1, Days 3–5 | Phase C (pgvector + local embeddings) | Search actually works at scale |
| Week 2, Days 1–4 | Phase D1+D2+D3+D6 (semantic + temporal relationships + graph UI) | **The differentiator works** |
| Week 2, Days 5–7 | Phase G2+G3+H1+H2 (UX polish + demo dataset) | Demo-ready |

---

## Verification Plan

### Automated Tests
```bash
# Run existing test suite
cd backend && pytest tests/ -v

# New tests to add:
pytest tests/test_pgvector_search.py   # Phase C
pytest tests/test_relationships_v2.py  # Phase D (semantic + temporal)
pytest tests/test_deduplication.py     # Phase F
pytest tests/test_pipeline_e2e.py      # Full pipeline integration test
```

### Manual Verification
1. Upload 10 real screenshots → verify pipeline completes all 5 stages
2. Search "CUDA" → verify screenshot with CUDA error appears first
3. Upload 2 screenshots from the same domain → verify domain relationship created
4. Upload screenshots 30 min apart → verify temporal relationship created  
5. Open Connections page → verify interactive graph renders with nodes/edges
6. Click a node → verify 1-hop neighborhood highlights
7. Chat: "What Python errors did I encounter?" → verify RAG answer with screenshot citations
8. Check Memory Detail page → verify "Related Screenshots" panel shows linked memories with explanation

---

## Architecture After All Phases Complete

```
Upload / Folder Watch
        ↓
   Ingest API (dedup check)
        ↓
   Pipeline (async queue)
   ├── Preprocessing (EXIF → captured_at)
   ├── OCR (PaddleOCR / LLM)
   ├── AI Extraction (Gemini/Groq → title, summary, entities, tags, app, domain)
   ├── Embedding (SentenceTransformers local / Gemini → pgvector)
   └── Relationships (entity + semantic + temporal + domain)
        ↓
   PostgreSQL + pgvector
   ├── screenshots
   ├── memories (+ embedding vector(768))
   ├── entities (normalized)
   ├── relationships (all 4 types)
   ├── projects (auto-detected)
   └── stories (temporal clusters)
        ↓
   FastAPI + React
   ├── Search: pgvector ANN + pg full-text → hybrid score
   ├── Connections: react-force-graph with 4 node types
   ├── Chat: RAG over memories + projects + stories
   ├── Timeline: captured_at + calendar heatmap
   └── Insights: real metrics (no hardcoded numbers)
```
