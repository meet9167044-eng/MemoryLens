# MemoryLens — Final Backend Architecture & Execution Plan

> **Objective:** Transition MemoryLens backend from external compute/Kaggle dependency into a self-contained, lightning-fast, production-ready system. Users upload files directly to their local/cloud dataset, and a unified Multimodal LLM + pgvector pipeline handles OCR, semantic extraction, entity resolution, relationship linking, hybrid search, and interactive memory chat.

---

## 1. Executive Summary & Architectural Shift

### 1.1 Why Kaggle is No Longer Needed
In earlier concepts, running heavy open-source vision/OCR/embedding models required GPU notebooks (such as Kaggle or Google Colab) and manual data export/import workflows. 

By upgrading to modern **Multimodal LLMs (e.g., Google Gemini 1.5/2.0 Flash or OpenAI GPT-4o-mini)** paired with **Cloud/Lightweight Embeddings (`text-embedding-004` / FastEmbed)** and **PostgreSQL (`pgvector`)**, we achieve:
1. **Zero External Notebooks / Zero Manual Sync:** Everything runs synchronously or in FastAPI background threads on the local machine/server.
2. **Superior Accuracy & Speed:** A single multimodal LLM call extracts full OCR text, contextual title, executive summary, semantic tags, and typed entities in < 1.5 seconds.
3. **Ultra-lightweight Server Footprint:** No 5GB+ CUDA/PyTorch/PaddlePaddle dependencies required locally unless running offline fallback.
4. **Direct Dataset Ingestion:** Uploaded files (screenshots, images, PDFs, code snippets, notes) are saved directly into the user's persistent dataset directory with automatic SHA-256 deduplication and database indexing.

---

## 2. System Architecture Diagram

```mermaid
flowchart TD
    subgraph Frontend["React + TypeScript UI"]
        UI_Upload["File Upload Dropzone\n(Images / Screenshots / Docs)"]
        UI_Browse["Memory Explorer &\nDetail Views"]
        UI_Search["Hybrid Search Bar"]
        UI_Chat["MemoryLens AI Chat\n(Ask Your Memories)"]
    end

    subgraph FastAPI_Backend["FastAPI Backend (Port 8000)"]
        API_Ingest["/api/v1/ingest/upload"]
        API_Memories["/api/v1/memories"]
        API_Search["/api/v1/search/hybrid"]
        API_Chat["/api/v1/chat"]

        subgraph Background_Pipeline["Async Ingestion Pipeline"]
            P_Storage["1. Dataset Storage &\nDeduplication (SHA-256)"]
            P_LLM["2. Multimodal LLM Engine\n(OCR + Summary + Entities)"]
            P_Embed["3. Vector Embedding Engine\n(Gemini / OpenAI / FastEmbed)"]
            P_Graph["4. Relationship & Graph Engine\n(Temporal + Entity + Vector)"]
        end
    end

    subgraph Storage_Layer["Storage & Data Layer"]
        Dataset_Dir["Dataset Storage Folder\n(/data/dataset/ or /uploads/)"]
        PG_DB[("PostgreSQL Database")]
        PG_Vector["pgvector Extension\n(HNSW Cosine Index)"]
        PG_FTS["PostgreSQL Full-Text Search\n(tsvector / BM25)"]
    end

    subgraph LLM_Cloud["AI Services"]
        LLM_Vision["Multimodal Vision LLM\n(Gemini 2.0 / 1.5 Flash / GPT-4o-mini)"]
        LLM_Embed["Embedding Model\n(text-embedding-004)"]
    end

    UI_Upload --> API_Ingest
    API_Ingest --> P_Storage
    P_Storage --> Dataset_Dir
    P_Storage --> P_LLM
    P_LLM --> LLM_Vision
    LLM_Vision --> P_LLM
    P_LLM --> P_Embed
    P_Embed --> LLM_Embed
    LLM_Embed --> P_Embed
    P_Embed --> P_Graph
    P_Graph --> PG_DB

    PG_DB --> PG_Vector
    PG_DB --> PG_FTS

    UI_Browse --> API_Memories
    API_Memories --> PG_DB

    UI_Search --> API_Search
    API_Search --> PG_Vector
    API_Search --> PG_FTS

    UI_Chat --> API_Chat
    API_Chat --> PG_Vector
    API_Chat --> LLM_Vision
```

---

## 3. Dataset & File Storage Structure

Uploaded files are preserved in a structured dataset hierarchy that ensures files are never lost, corrupted, or duplicated.

```
backend/
├── data/
│   └── dataset/
│       ├── raw/                       # Original high-res uploaded files
│       │   └── 2026/
│       │       └── 08/
│       │           ├── mem_9a8f2e_screenshot.png
│       │           └── mem_4b7c1d_code_snippet.jpg
│       ├── thumbnails/                # Compressed web-optimized thumbnails (webp)
│       │   └── mem_9a8f2e_thumb.webp
│       └── metadata_cache/            # JSON sidecar files for export/backup
│           └── mem_9a8f2e.json
```

### Ingestion Specifications:
- **Deduplication:** Compute SHA-256 hash on upload. If identical file exists, return existing `memory_id` without wasting LLM compute.
- **Image Optimization:** Generate a fast 400px WEBP thumbnail for gallery view while keeping full resolution for Detail zoom.
- **Supported Media:** PNG, JPG, JPEG, WEBP, PDF (rendered to images), Text/Markdown files.

---

## 4. Multimodal LLM Processing Engine

Instead of running separate OCR (PaddleOCR), separate Summarizers (BART), and separate NER models (Spacy) on Kaggle GPUs, a **single structured LLM call** extracts rich, structured metadata with high fidelity.

### 4.1 Extraction Schema (Pydantic / JSON Structured Output)
```json
{
  "title": "Configuring CUDA Acceleration in PyTorch",
  "summary": "User troubleshooting torch.cuda.is_available() returning False inside VS Code terminal on Windows.",
  "ocr_text": ">>> import torch\n>>> torch.cuda.is_available()\nFalse\nCUDA_PATH=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1",
  "app_detected": "VS Code",
  "source_type": "terminal",
  "entities": [
    {"name": "PyTorch", "type": "framework"},
    {"name": "CUDA", "type": "technology"},
    {"name": "VS Code", "type": "tool"},
    {"name": "NVIDIA", "type": "company"}
  ],
  "tags": ["cuda", "gpu-debugging", "pytorch", "environment-setup"],
  "action_items": [
    "Verify NVIDIA drivers and reinstall PyTorch with matching cu121 wheel"
  ],
  "confidence": 0.96
}
```

### 4.2 Fallback Strategy
- **Primary:** Google Gemini 1.5/2.0 Flash API (Ultra fast ~800ms, multimodal, cost-effective).
- **Secondary:** OpenAI GPT-4o-mini API.
- **Offline / Local Fallback:** Tesseract / PaddleOCR + rule-based entity extractor if no internet/API key is present.

---

## 5. Embeddings & Hybrid Search Strategy

### 5.1 Embedding Generation
- Text embedding is generated from a composite representation:
  `"{title} | {summary} | Tags: {tags} | Entities: {entities} | Text: {ocr_text[:500]}"`
- **Embedding Dimensions:** 768 (Gemini `text-embedding-004`) or 1536 (OpenAI `text-embedding-3-small`).

### 5.2 PostgreSQL Hybrid Search (pgvector + FTS)
Combine Vector Cosine Similarity and PostgreSQL Full-Text Keyword Search via **Reciprocal Rank Fusion (RRF)**:

$$\text{RRF Score}(d) = \frac{w_{\text{vec}}}{60 + r_{\text{vec}}(d)} + \frac{w_{\text{text}}}{60 + r_{\text{text}}(d)}$$

```sql
-- Hybrid Search Query
WITH vector_matches AS (
    SELECT id, RANK() OVER (ORDER BY embedding <=> :query_vector) AS rank_vec
    FROM memories
    WHERE embedding IS NOT NULL
    LIMIT 50
),
text_matches AS (
    SELECT id, RANK() OVER (ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query_text)) DESC) AS rank_text
    FROM memories
    WHERE search_vector @@ plainto_tsquery('english', :query_text)
    LIMIT 50
)
SELECT m.*,
       (COALESCE(1.0 / (60 + v.rank_vec), 0.0) * 0.6 +
        COALESCE(1.0 / (60 + t.rank_text), 0.0) * 0.4) AS hybrid_score
FROM memories m
LEFT JOIN vector_matches v ON m.id = v.id
LEFT JOIN text_matches t ON m.id = t.id
WHERE v.id IS NOT NULL OR t.id IS NOT NULL
ORDER BY hybrid_score DESC
LIMIT :limit OFFSET :offset;
```

---

## 6. Relationship & Memory Graph Engine

Every new memory is automatically linked to related memories in the dataset across 4 dimensions:

1. **Temporal Proximity:** Memories captured within 15–30 minutes in the same application.
2. **Entity Overlap:** Memories sharing high-importance entities (e.g., both mention `MemoryLens` and `pgvector`).
3. **Semantic Similarity:** Cosine similarity $> 0.82$ on vector embeddings.
4. **Error / Topic Correlation:** Matching debug logs or repeated code patterns.

These links populate the `related_memories` table to power the **Connections** screen and contextual suggestions.

---

## 7. MemoryLens AI Chat & RAG Assistant

Users can query their entire digital history naturally:
> *"When was the last time I debugged that CUDA installation error, and what command fixed it?"*

### RAG Flow:
1. **Query Embedding & Retrieval:** Search vector store for top-5 relevant memories + filter by mentioned entities/dates.
2. **Context Assembly:** Inject memory snapshots (timestamp, title, summary, OCR snippet, source app) into LLM system prompt.
3. **Grounded Answer Generation:** The LLM produces a concise, accurate response with clickable memory citations `[Memory #12 - 10:45 AM]`.

---

## 8. Complete API Endpoint Specifications

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/ingest/upload` | Multi-file/Single-file upload to dataset with async background processing |
| `GET` | `/api/v1/ingest/status/{job_id}` | Check real-time progress (`QUEUED`, `LLM_EXTRACTING`, `EMBEDDING`, `COMPLETED`) |
| `GET` | `/api/v1/memories` | Paginated list of memories with filters (app, tag, entity, date range) |
| `GET` | `/api/v1/memories/{id}` | Detailed memory profile with full OCR, entities, tags, and related memories |
| `DELETE` | `/api/v1/memories/{id}` | Remove memory and clean up dataset files |
| `POST` | `/api/v1/search/hybrid` | Hybrid semantic + full-text search with highlighting |
| `GET` | `/api/v1/timeline` | Chronological grouped feed (by day/hour) |
| `GET` | `/api/v1/connections` | Nodes and edges graph data for entity & memory visualizer |
| `GET` | `/api/v1/insights` | Auto-generated productivity trends, common topics, and debug session clusters |
| `POST` | `/api/v1/chat` | RAG conversational assistant over user memories |

---

## 9. Implementation Roadmap & Execution Phases

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND EXECUTION PHASES                        │
├───────────────────┬────────────────────────────────────────────────────┤
│ Phase A           │ Dataset Storage & Direct Ingestion Engine          │
│ Phase B           │ Multimodal LLM Extraction Provider (Gemini/OpenAI) │
│ Phase C           │ pgvector Embedding & Hybrid RRF Search Service     │
│ Phase D           │ Relationship Engine & Graph Generation             │
│ Phase E           │ Conversational RAG Chat Endpoint                   │
│ Phase F           │ Frontend API Connectors & Live Testing             │
└───────────────────┴────────────────────────────────────────────────────┘
```

### Phase A: Dataset Storage & Direct Ingestion Engine
- Implement `DatasetStorageManager` in `backend/app/core/dataset.py`.
- Handle file saves to `data/dataset/raw/` with date-based partitioning.
- Add automatic thumbnail generation with Pillow (`data/dataset/thumbnails/`).
- Add SHA-256 hash checks to prevent duplicate entries.

### Phase B: Multimodal LLM Extraction Provider
- Implement `LLMExtractor` in `backend/app/services/llm_extractor.py`.
- Configure Google Gemini 1.5/2.0 Flash API (or OpenAI GPT-4o-mini) with structured Pydantic response parsing.
- Extract: `title`, `summary`, `ocr_text`, `entities`, `tags`, `app_name`, `confidence`.
- Add local fallback if API keys are not supplied.

### Phase C: pgvector Embedding & Hybrid RRF Search Service
- Integrate `text-embedding-004` (or FastEmbed for 100% offline local embeddings).
- Populate the `embedding` column in PostgreSQL `memories` table.
- Implement `/api/v1/search/hybrid` with Reciprocal Rank Fusion combining `pgvector` distance and `tsvector` keyword matching.

### Phase D: Relationship Engine & Graph Generation
- Update `backend/app/processing/relationships.py` to auto-link memories post-ingestion.
- Expose `/api/v1/connections` returning `{ nodes: [...], edges: [...] }` matching the frontend graph visualizer.

### Phase E: Conversational RAG Chat Endpoint
- Create `/api/v1/chat` endpoint with streaming support.
- Retrieve top-5 relevant memories and synthesize direct answers with citations.

### Phase F: Frontend API Integration & Verification
- Connect React UI upload modal to `/api/v1/ingest/upload`.
- Bind search bar to `/api/v1/search/hybrid`.
- Connect Memory Explorer, Detail, Timeline, and Connections views to backend data.

---

## 10. Environment Variables (`.env`)

```ini
# App Configuration
APP_NAME=MemoryLens
ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0

# Database (PostgreSQL with pgvector)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/memorylens

# Dataset File Storage
DATASET_STORAGE_PATH=./data/dataset
MAX_UPLOAD_SIZE_MB=50

# AI / LLM Configuration (No Kaggle Needed)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Embedding Configuration
EMBEDDING_PROVIDER=gemini
EMBEDDING_MODEL=text-embedding-004
EMBEDDING_DIMENSIONS=768
```

---

## 11. Summary of Benefits

1. **Self-Contained & Instant:** No external GPU notebook or batch export/import hurdles.
2. **True Multimodal AI:** OCR, summarization, entity extraction, and tagging happen in a single, high-speed LLM pass.
3. **Dataset First:** All user files are permanently organized, versioned, and indexed in the local dataset.
4. **Rich Experience:** Powers all 7 frontend views (Overview, Memories, Detail, Search, Timeline, Connections, Insights) + conversational AI chat.
