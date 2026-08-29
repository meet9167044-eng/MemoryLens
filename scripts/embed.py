import json
import time
from sentence_transformers import SentenceTransformer, util

# ──────────────────────────────────────────────────────────
# PHASE 7 — MemoryLens Multimodal Embeddings
#
# Uses a local pre-trained SentenceTransformer model from
# Hugging Face ('all-MiniLM-L6-v2') to convert structured
# Memory text into 384-dimensional vector embeddings.
# ──────────────────────────────────────────────────────────

MODEL_NAME = "all-MiniLM-L6-v2"

print(f"[Phase 7] Loading embedding model '{MODEL_NAME}'...")
start_time = time.time()
# Loads model locally (downloads ~90MB on first run, cached after)
model = SentenceTransformer(MODEL_NAME)
print(f"[Phase 7] Model loaded in {time.time() - start_time:.2f} seconds!")

# ── SAMPLE MEMORY INPUT (Simulates output from Phase 6) ───
SAMPLE_MEMORY_DATA = {
    "title": "RuntimeError: CUDA out of memory. Tried to allocate 1.45 GiB",
    "summary": "A PyTorch process exceeded available GPU memory during training.",
    "ocr_text": "RuntimeError: CUDA out of memory. Tried to allocate 1.45 GiB (GPU 0; 8.00 GiB total capacity)",
    "entities": ["CUDA", "GPU", "PyTorch", "NVIDIA", "Python"],
    "tags": ["cuda", "error", "gpu", "memory", "python", "pytorch"]
}


def prepare_embedding_text(memory_data: dict) -> str:
    """
    Constructs a rich, normalized text representation of the Memory
    combining Title, Summary, Entities, Tags, and OCR text.
    """
    title = memory_data.get("title") or ""
    summary = memory_data.get("summary") or ""
    ocr_text = memory_data.get("ocr_text") or ""
    entities = ", ".join(memory_data.get("entities", []))
    tags = ", ".join(memory_data.get("tags", []))

    # Combine all semantic signals into one document string
    combined_text = f"Title: {title}\nSummary: {summary}\nEntities: {entities}\nTags: {tags}\nContent: {ocr_text}"
    return combined_text.strip()


def generate_text_embedding(memory_data: dict) -> dict:
    """
    PHASE 7 — MemoryLens Embedding Generation

    Args:
        memory_data : Structured Memory dictionary (from Phase 6)

    Returns:
        Dictionary containing vector array, dimension, model info
    """
    result = {
        "model_name": MODEL_NAME,
        "embedding_dim": None,
        "vector": [],
        "success": False,
        "error": None
    }

    try:
        # 1. Prepare combined semantic text
        text_to_embed = prepare_embedding_text(memory_data)

        # 2. Generate vector embedding
        start_embed = time.time()
        embedding_vector = model.encode(text_to_embed).tolist()
        elapsed = time.time() - start_embed

        result["vector"] = embedding_vector
        result["embedding_dim"] = len(embedding_vector)
        result["success"] = True

        print(f"[Phase 7] ✅ Generated {result['embedding_dim']}-dim vector in {elapsed:.4f} seconds!")

    except Exception as e:
        result["error"] = str(e)
        print(f"[Phase 7] ❌ Error: {e}")

    return result


def test_similarity():
    """
    Simulates Phase 8 (Semantic Search) by comparing user queries
    against the generated Memory vector using Cosine Similarity.
    """
    print("\n── SIMILARITY SEARCH TEST ──────────────────────────")

    memory_text = prepare_embedding_text(SAMPLE_MEMORY_DATA)
    memory_vec = model.encode(memory_text, convert_to_tensor=True)

    queries = [
        "Where was my CUDA out of memory error?",
        "Show me my GPU memory crash from PyTorch",
        "Python script failed on graphics card",
        "How to make a delicious recipe for dinner?"
    ]

    print("Querying against sample Memory vector...\n")
    for q in queries:
        q_vec = model.encode(q, convert_to_tensor=True)
        # Compute Cosine Similarity (0.0 = completely unrelated, 1.0 = identical)
        similarity = util.cos_sim(memory_vec, q_vec).item()
        print(f"Query     : '{q}'")
        print(f"Similarity: {similarity:.4f} ({similarity * 100:.1f}% match)")
        print("-" * 50)


# ── RUN MAIN ──────────────────────────────────────────────
if __name__ == "__main__":
    print("── Phase 7: Text Embedding Generation ──────────────\n")

    result = generate_text_embedding(SAMPLE_MEMORY_DATA)

    print("\n── RESULT SUMMARY ──────────────────────────────────")
    print(f"Success       : {result['success']}")
    print(f"Model         : {result['model_name']}")
    print(f"Vector Dim    : {result['embedding_dim']}")
    print(f"Sample Vector : {result['vector'][:5]}... (first 5 of {len(result['vector'])})")

    test_similarity()