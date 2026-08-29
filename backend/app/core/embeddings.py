"""
Lightweight embedding utility for Phase 8 synthetic-data backend.

Production path: swap `embed_text` to call a real Sentence-Transformer
or pgvector-stored vectors.  The cosine_similarity helper is model-agnostic
and stays unchanged.

No external ML libraries are required here — the vocabulary is built from
the synthetic dataset, making TF-IDF-style vectors good enough to demonstrate
semantic recall (e.g. "GPU problem" → finds "CUDA out of memory" memory).
"""

from __future__ import annotations
import math
import re
from functools import lru_cache
from typing import List


# ---------------------------------------------------------------------------
# Vocabulary — terms that carry semantic weight across the synthetic dataset
# ---------------------------------------------------------------------------
_VOCAB: List[str] = [
    # GPU / ML
    "cuda", "gpu", "memory", "pytorch", "torch", "nvidia", "driver",
    "vram", "out", "error", "runtime", "allocate", "training", "model",
    "deep", "learning", "ml", "neural", "network", "tensor",
    # Python / code
    "python", "code", "script", "import", "module", "pip", "conda",
    "virtualenv", "venv", "debug", "traceback", "exception", "stack",
    "overflow", "stackoverflow", "terminal", "bash", "shell",
    # Web / browser
    "chrome", "browser", "website", "url", "http", "api", "rest",
    "frontend", "react", "vite", "typescript", "css", "html",
    # Tools / apps
    "vscode", "code", "editor", "jupyter", "notebook", "figma",
    "slack", "github", "git", "commit", "branch", "pull", "request",
    # Project / work
    "internship", "application", "resume", "recruiter", "interview",
    "linkedin", "job", "project", "deadline", "meeting", "notes",
    # MemoryLens-specific
    "memorylens", "memory", "search", "semantic", "embedding", "ocr",
    "screenshot", "capture", "devjam", "hackathon",
    # General
    "install", "setup", "configure", "settings", "update", "version",
    "fix", "solution", "problem", "issue", "help", "document", "pdf",
]

_VOCAB_INDEX = {term: idx for idx, term in enumerate(_VOCAB)}
_VOCAB_SIZE = len(_VOCAB)


def _tokenize(text: str) -> List[str]:
    """Lower-case, split on non-alpha-numeric, strip empties."""
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


@lru_cache(maxsize=512)
def embed_text(text: str) -> tuple:
    """
    Return a normalised bag-of-words vector (as a tuple for hashability/caching)
    aligned to _VOCAB.

    Args:
        text: Any string (query or memory document).

    Returns:
        Tuple of floats of length _VOCAB_SIZE.  The vector is L2-normalised
        so cosine_similarity is equivalent to dot product.
    """
    vec = [0.0] * _VOCAB_SIZE
    tokens = _tokenize(text)
    for token in tokens:
        if token in _VOCAB_INDEX:
            vec[_VOCAB_INDEX[token]] += 1.0

    # L2 normalise
    magnitude = math.sqrt(sum(v * v for v in vec))
    if magnitude > 0:
        vec = [v / magnitude for v in vec]

    return tuple(vec)


def cosine_similarity(a: tuple, b: tuple) -> float:
    """
    Cosine similarity between two L2-normalised vectors.
    Equivalent to dot product when both are already normalised.

    Args:
        a: First vector (output of embed_text).
        b: Second vector (output of embed_text).

    Returns:
        Float in [0.0, 1.0].
    """
    return sum(x * y for x, y in zip(a, b))
