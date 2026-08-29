"""
Synthetic in-memory dataset for Phase 8.

This mirrors src/data/mockMemories.ts so the backend API produces results
consistent with what the frontend already renders.

Required memory mem_1827 (from docs/SYNTHETIC_DATA.md) is included verbatim.
Scale: 20 memories — architecture supports 60-100 seamlessly.

Production swap: replace SYNTHETIC_MEMORIES with a DB query that returns
the same dict structure from the `memories` + `embeddings` tables.
"""

from __future__ import annotations
from typing import List, Dict, Any

SYNTHETIC_MEMORIES: List[Dict[str, Any]] = [
    # ── 1 ── (REQUIRED by SYNTHETIC_DATA.md) ────────────────────────────────
    {
        "id": "mem_1827",
        "timestamp": "2026-01-14T10:32:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1827", "imageUrl": "/synthetic/screenshots/1827.png"},
        "content": {
            "ocrText": "RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB "
                       "(GPU 0; 8.00 GiB total capacity; 6.12 GiB already allocated; "
                       "512.00 MiB free).",
            "title": "CUDA Out of Memory Error",
            "summary": "A PyTorch process exceeded available GPU memory while training a model.",
        },
        "entities": [
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
            {"id": "entity_pytorch", "name": "PyTorch", "type": "framework"},
            {"id": "entity_nvidia", "name": "NVIDIA", "type": "company"},
        ],
        "tags": ["error", "gpu", "python", "pytorch", "cuda"],
        "relatedMemories": [
            {"memoryId": "mem_1842", "relationship": "same_topic", "similarityScore": 0.91},
            {"memoryId": "mem_1809", "relationship": "related_error", "similarityScore": 0.87},
        ],
        "metadata": {"language": "en", "contentType": "error", "confidence": 0.96},
    },

    # ── 2 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1809",
        "timestamp": "2026-01-12T14:15:00",
        "source": {"app": "Terminal", "type": "terminal"},
        "screenshot": {"id": "1809", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "nvidia-smi: NVIDIA driver not found. Please install the appropriate "
                       "NVIDIA driver for your GPU.",
            "title": "NVIDIA Driver Missing",
            "summary": "Attempt to run nvidia-smi failed — driver not installed.",
        },
        "entities": [
            {"id": "entity_nvidia", "name": "NVIDIA", "type": "company"},
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
        ],
        "tags": ["driver", "nvidia", "gpu", "terminal", "error"],
        "relatedMemories": [
            {"memoryId": "mem_1827", "relationship": "related_error", "similarityScore": 0.87},
        ],
        "metadata": {"language": "en", "contentType": "error", "confidence": 0.94},
    },

    # ── 3 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1842",
        "timestamp": "2026-01-15T09:00:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1842", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Stack Overflow: How to fix CUDA out of memory in PyTorch? "
                       "Answer: Reduce batch size or use torch.cuda.empty_cache().",
            "title": "Stack Overflow — CUDA Memory Fix",
            "summary": "Stack Overflow answer explaining how to resolve GPU OOM in PyTorch.",
        },
        "entities": [
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
            {"id": "entity_pytorch", "name": "PyTorch", "type": "framework"},
            {"id": "entity_stackoverflow", "name": "Stack Overflow", "type": "tool"},
        ],
        "tags": ["stackoverflow", "cuda", "gpu", "python", "fix"],
        "relatedMemories": [
            {"memoryId": "mem_1827", "relationship": "same_topic", "similarityScore": 0.91},
        ],
        "metadata": {"language": "en", "contentType": "reference", "confidence": 0.92},
    },

    # ── 4 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1855",
        "timestamp": "2026-01-16T11:20:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1855", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Epoch 10/50  loss=0.2341  val_loss=0.3012  accuracy=0.914  "
                       "val_accuracy=0.891  — Training ResNet50 on CIFAR-10.",
            "title": "PyTorch Model Training — Epoch 10",
            "summary": "Successful training run of ResNet50 after fixing the CUDA OOM issue.",
        },
        "entities": [
            {"id": "entity_pytorch", "name": "PyTorch", "type": "framework"},
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
        ],
        "tags": ["training", "ml", "pytorch", "success", "resnet"],
        "relatedMemories": [
            {"memoryId": "mem_1827", "relationship": "same_topic", "similarityScore": 0.85},
        ],
        "metadata": {"language": "en", "contentType": "progress", "confidence": 0.98},
    },

    # ── 5 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1770",
        "timestamp": "2026-01-08T16:00:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1770", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "CUDA Toolkit 12.3 Installation Guide — Step 1: Verify GPU compatibility. "
                       "Step 2: Download the installer. Step 3: Run the installer.",
            "title": "CUDA Toolkit Installation Guide",
            "summary": "Official NVIDIA CUDA Toolkit 12.3 installation instructions.",
        },
        "entities": [
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
            {"id": "entity_nvidia", "name": "NVIDIA", "type": "company"},
        ],
        "tags": ["cuda", "install", "setup", "nvidia", "gpu"],
        "relatedMemories": [
            {"memoryId": "mem_1809", "relationship": "same_topic", "similarityScore": 0.82},
        ],
        "metadata": {"language": "en", "contentType": "document", "confidence": 0.97},
    },

    # ── 6 ── Internship ───────────────────────────────────────────────────────
    {
        "id": "mem_1630",
        "timestamp": "2026-01-03T10:00:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1630", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Google Summer Internship 2026 — Software Engineering Intern. "
                       "Location: Bangalore. Deadline: Jan 20, 2026.",
            "title": "Google Internship Posting",
            "summary": "Google SWE intern role for summer 2026 with Bangalore location.",
        },
        "entities": [
            {"id": "entity_google", "name": "Google", "type": "company"},
        ],
        "tags": ["internship", "job", "google", "application"],
        "relatedMemories": [
            {"memoryId": "mem_1635", "relationship": "same_project", "similarityScore": 0.93},
        ],
        "metadata": {"language": "en", "contentType": "opportunity", "confidence": 0.95},
    },

    # ── 7 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1635",
        "timestamp": "2026-01-04T14:30:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1635", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Google Careers — Submit your application. Your resume has been uploaded. "
                       "Referral code applied. Click Submit.",
            "title": "Google Application Portal",
            "summary": "Application portal for the Google SWE internship — ready to submit.",
        },
        "entities": [
            {"id": "entity_google", "name": "Google", "type": "company"},
        ],
        "tags": ["internship", "application", "google", "portal"],
        "relatedMemories": [
            {"memoryId": "mem_1630", "relationship": "same_project", "similarityScore": 0.93},
            {"memoryId": "mem_1650", "relationship": "same_project", "similarityScore": 0.88},
        ],
        "metadata": {"language": "en", "contentType": "form", "confidence": 0.97},
    },

    # ── 8 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1650",
        "timestamp": "2026-01-09T09:15:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1650", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "LinkedIn — Google Recruiter: Hi! I saw your profile and would love "
                       "to discuss the SWE intern opportunity. Are you available for a call?",
            "title": "Google Recruiter LinkedIn Message",
            "summary": "Recruiter from Google reached out on LinkedIn about the internship.",
        },
        "entities": [
            {"id": "entity_google", "name": "Google", "type": "company"},
            {"id": "entity_linkedin", "name": "LinkedIn", "type": "tool"},
        ],
        "tags": ["internship", "recruiter", "linkedin", "google", "message"],
        "relatedMemories": [
            {"memoryId": "mem_1635", "relationship": "same_project", "similarityScore": 0.88},
            {"memoryId": "mem_1660", "relationship": "same_project", "similarityScore": 0.91},
        ],
        "metadata": {"language": "en", "contentType": "communication", "confidence": 0.96},
    },

    # ── 9 ── ─────────────────────────────────────────────────────────────────
    {
        "id": "mem_1660",
        "timestamp": "2026-01-15T11:00:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1660", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Google Interview Invitation — You are invited to complete an online "
                       "technical assessment. Deadline: Jan 22, 2026. Duration: 90 minutes.",
            "title": "Google Interview Invitation",
            "summary": "Online technical assessment invitation from Google for the SWE role.",
        },
        "entities": [
            {"id": "entity_google", "name": "Google", "type": "company"},
        ],
        "tags": ["internship", "interview", "google", "assessment"],
        "relatedMemories": [
            {"memoryId": "mem_1650", "relationship": "same_project", "similarityScore": 0.91},
        ],
        "metadata": {"language": "en", "contentType": "invitation", "confidence": 0.98},
    },

    # ── 10 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1902",
        "timestamp": "2026-01-20T15:00:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1902", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "MemoryLens/src/data/mockMemories.ts — export const mockMemories: Memory[] = ["
                       "  { id: 'mem_1827', timestamp: '2026-01-14T10:32:00', ... }",
            "title": "MemoryLens Frontend — mockMemories.ts",
            "summary": "Working on the synthetic data file for the MemoryLens frontend prototype.",
        },
        "entities": [
            {"id": "entity_memorylens", "name": "MemoryLens", "type": "project"},
            {"id": "entity_typescript", "name": "TypeScript", "type": "technology"},
            {"id": "entity_react", "name": "React", "type": "framework"},
        ],
        "tags": ["memorylens", "frontend", "typescript", "development"],
        "relatedMemories": [
            {"memoryId": "mem_1910", "relationship": "same_project", "similarityScore": 0.94},
        ],
        "metadata": {"language": "en", "contentType": "code", "confidence": 0.99},
    },

    # ── 11 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1910",
        "timestamp": "2026-01-21T10:30:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1910", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "MemoryLens — DevJam Hackathon Submission. "
                       "Search your digital memory. Semantic screenshot retrieval.",
            "title": "MemoryLens DevJam Submission",
            "summary": "DevJam hackathon project page for MemoryLens.",
        },
        "entities": [
            {"id": "entity_memorylens", "name": "MemoryLens", "type": "project"},
            {"id": "entity_devjam", "name": "DevJam", "type": "topic"},
        ],
        "tags": ["memorylens", "hackathon", "devjam", "submission"],
        "relatedMemories": [
            {"memoryId": "mem_1902", "relationship": "same_project", "similarityScore": 0.94},
        ],
        "metadata": {"language": "en", "contentType": "project", "confidence": 0.97},
    },

    # ── 12 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1740",
        "timestamp": "2026-01-07T08:45:00",
        "source": {"app": "Jupyter", "type": "desktop"},
        "screenshot": {"id": "1740", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "import torch\nprint(torch.__version__)  # 2.2.0+cu121\n"
                       "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n"
                       "print(device)  # cuda",
            "title": "PyTorch CUDA Setup Check",
            "summary": "Jupyter notebook verifying that PyTorch detects the CUDA GPU correctly.",
        },
        "entities": [
            {"id": "entity_pytorch", "name": "PyTorch", "type": "framework"},
            {"id": "entity_cuda", "name": "CUDA", "type": "technology"},
            {"id": "entity_jupyter", "name": "Jupyter", "type": "tool"},
        ],
        "tags": ["pytorch", "cuda", "jupyter", "setup", "python"],
        "relatedMemories": [
            {"memoryId": "mem_1827", "relationship": "same_topic", "similarityScore": 0.80},
        ],
        "metadata": {"language": "en", "contentType": "code", "confidence": 0.98},
    },

    # ── 13 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1801",
        "timestamp": "2026-01-11T13:00:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1801", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Traceback (most recent call last):\n  File 'train.py', line 47\n"
                       "ImportError: No module named 'torchvision'",
            "title": "Python ImportError — torchvision Missing",
            "summary": "ImportError in training script caused by missing torchvision package.",
        },
        "entities": [
            {"id": "entity_pytorch", "name": "PyTorch", "type": "framework"},
            {"id": "entity_python", "name": "Python", "type": "technology"},
        ],
        "tags": ["error", "python", "import", "torchvision", "debug"],
        "relatedMemories": [
            {"memoryId": "mem_1827", "relationship": "same_topic", "similarityScore": 0.74},
        ],
        "metadata": {"language": "en", "contentType": "error", "confidence": 0.95},
    },

    # ── 14 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1950",
        "timestamp": "2026-01-22T16:20:00",
        "source": {"app": "Figma", "type": "desktop"},
        "screenshot": {"id": "1950", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "MemoryLens UI Design — Search Page. Dark mode. "
                       "Search bar with gradient glow. Memory cards grid layout.",
            "title": "MemoryLens UI Design — Search Page",
            "summary": "Figma design iteration for the MemoryLens search interface.",
        },
        "entities": [
            {"id": "entity_memorylens", "name": "MemoryLens", "type": "project"},
            {"id": "entity_figma", "name": "Figma", "type": "tool"},
        ],
        "tags": ["design", "ui", "figma", "memorylens", "search"],
        "relatedMemories": [
            {"memoryId": "mem_1902", "relationship": "same_project", "similarityScore": 0.89},
        ],
        "metadata": {"language": "en", "contentType": "design", "confidence": 0.96},
    },

    # ── 15 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1600",
        "timestamp": "2026-01-01T20:00:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1600", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "git commit -m 'feat: add vector search endpoint with pgvector'\n"
                       "git push origin feature/phase-8-search",
            "title": "Git — Push Phase 8 Search Feature",
            "summary": "Terminal showing a git commit and push for the search feature branch.",
        },
        "entities": [
            {"id": "entity_git", "name": "Git", "type": "tool"},
            {"id": "entity_memorylens", "name": "MemoryLens", "type": "project"},
        ],
        "tags": ["git", "commit", "push", "search", "backend"],
        "relatedMemories": [
            {"memoryId": "mem_1902", "relationship": "same_project", "similarityScore": 0.76},
        ],
        "metadata": {"language": "en", "contentType": "terminal", "confidence": 0.99},
    },

    # ── 16 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1680",
        "timestamp": "2026-01-10T09:30:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1680", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "FastAPI documentation — Path Parameters. "
                       "GET /items/{item_id}  — returns {item_id: 5, q: 'somequery'}",
            "title": "FastAPI Docs — Path Parameters",
            "summary": "Reading FastAPI documentation on path parameters and query params.",
        },
        "entities": [
            {"id": "entity_fastapi", "name": "FastAPI", "type": "framework"},
            {"id": "entity_python", "name": "Python", "type": "technology"},
        ],
        "tags": ["fastapi", "api", "python", "documentation", "backend"],
        "relatedMemories": [],
        "metadata": {"language": "en", "contentType": "document", "confidence": 0.97},
    },

    # ── 17 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1710",
        "timestamp": "2026-01-11T15:45:00",
        "source": {"app": "Chrome", "type": "browser"},
        "screenshot": {"id": "1710", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "pgvector — Open-source vector similarity search for Postgres. "
                       "CREATE EXTENSION vector; ALTER TABLE items ADD COLUMN embedding vector(1536);",
            "title": "pgvector GitHub README",
            "summary": "pgvector README showing how to add vector columns to PostgreSQL.",
        },
        "entities": [
            {"id": "entity_pgvector", "name": "pgvector", "type": "tool"},
            {"id": "entity_postgres", "name": "PostgreSQL", "type": "technology"},
        ],
        "tags": ["pgvector", "database", "vector", "search", "postgresql"],
        "relatedMemories": [],
        "metadata": {"language": "en", "contentType": "document", "confidence": 0.98},
    },

    # ── 18 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1720",
        "timestamp": "2026-01-12T08:00:00",
        "source": {"app": "VS Code", "type": "desktop"},
        "screenshot": {"id": "1720", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "backend/app/processing/embeddings/text_embedder.py\n"
                       "class TextEmbeddingProvider:\n"
                       "    def embed(self, text: str) -> List[float]:",
            "title": "MemoryLens — Text Embedding Provider",
            "summary": "Writing the TextEmbeddingProvider class for Phase 7.",
        },
        "entities": [
            {"id": "entity_memorylens", "name": "MemoryLens", "type": "project"},
            {"id": "entity_python", "name": "Python", "type": "technology"},
        ],
        "tags": ["embedding", "python", "backend", "memorylens", "ml"],
        "relatedMemories": [
            {"memoryId": "mem_1710", "relationship": "same_project", "similarityScore": 0.78},
        ],
        "metadata": {"language": "en", "contentType": "code", "confidence": 0.98},
    },

    # ── 19 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1560",
        "timestamp": "2026-12-28T11:00:00",
        "source": {"app": "Slack", "type": "desktop"},
        "screenshot": {"id": "1560", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "DevJam #announcements: Registration is now open for DevJam 2026! "
                       "Theme: AI-powered personal tools. Submit by Feb 1.",
            "title": "DevJam 2026 Announcement",
            "summary": "Slack announcement for DevJam 2026 hackathon registration opening.",
        },
        "entities": [
            {"id": "entity_devjam", "name": "DevJam", "type": "topic"},
            {"id": "entity_slack", "name": "Slack", "type": "tool"},
        ],
        "tags": ["devjam", "hackathon", "announcement", "slack", "ai"],
        "relatedMemories": [
            {"memoryId": "mem_1910", "relationship": "same_topic", "similarityScore": 0.82},
        ],
        "metadata": {"language": "en", "contentType": "communication", "confidence": 0.95},
    },

    # ── 20 ── ────────────────────────────────────────────────────────────────
    {
        "id": "mem_1980",
        "timestamp": "2026-01-25T14:00:00",
        "source": {"app": "PDF Viewer", "type": "document"},
        "screenshot": {"id": "1980", "imageUrl": "/synthetic/screenshots/generic.png"},
        "content": {
            "ocrText": "Research Paper: Attention Is All You Need — Vaswani et al. (2017). "
                       "Abstract: The dominant sequence transduction models are based on complex "
                       "recurrent or convolutional neural networks...",
            "title": "Attention Is All You Need — Transformer Paper",
            "summary": "Reading the original Transformer paper by Vaswani et al.",
        },
        "entities": [
            {"id": "entity_ml", "name": "Machine Learning", "type": "topic"},
            {"id": "entity_transformer", "name": "Transformer", "type": "technology"},
        ],
        "tags": ["research", "paper", "transformer", "ml", "deep-learning"],
        "relatedMemories": [
            {"memoryId": "mem_1855", "relationship": "same_topic", "similarityScore": 0.71},
        ],
        "metadata": {"language": "en", "contentType": "document", "confidence": 0.97},
    },
]
