import json
import time
from sentence_transformers import SentenceTransformer, util

# ──────────────────────────────────────────────────────────
# PHASE 12 — Search Quality Evaluation (Precision @ K)
# ──────────────────────────────────────────────────────────

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Test Queries with expected Memory IDs
TEST_BENCHMARKS = [
    {
        "query": "CUDA memory error in PyTorch",
        "expected_top_id": "mem_1827"
    },
    {
        "query": "PyTorch documentation on memory management",
        "expected_top_id": "mem_1842"
    },
    {
        "query": "nvidia-smi terminal status",
        "expected_top_id": "mem_1809"
    },
    {
        "query": "Google internship application confirmation",
        "expected_top_id": "mem_2001"
    },
    {
        "query": "Recruiter interview email",
        "expected_top_id": "mem_2002"
    }
]

def load_dataset(path="dataset.json"):
    with open(path, "r") as f:
        return json.load(f)

def run_search_evaluation():
    dataset = load_dataset()
    print(f"[Phase 12] Loaded {len(dataset)} Memories for evaluation.\n")

    # Embed all memories
    memory_vectors = []
    for item in dataset:
        text = f"Title: {item['content']['title']}\nSummary: {item['content']['summary']}\nContent: {item['content']['ocrText']}"
        vec = MODEL.encode(text, convert_to_tensor=True)
        memory_vectors.append((item['id'], vec))

    hits = 0
    total = len(TEST_BENCHMARKS)

    print("── SEARCH EVALUATION RESULTS ────────────────────────\n")
    for bench in TEST_BENCHMARKS:
        q_text = bench["query"]
        q_vec = MODEL.encode(q_text, convert_to_tensor=True)

        # Rank all memories
        scores = []
        for mem_id, m_vec in memory_vectors:
            sim = util.cos_sim(q_vec, m_vec).item()
            scores.append((mem_id, sim))

        # Sort by similarity descending
        scores.sort(key=lambda x: x[1], reverse=True)
        top_hit_id, top_score = scores[0]

        is_correct = (top_hit_id == bench["expected_top_id"])
        if is_correct:
            hits += 1

        status_icon = "✅ PASS" if is_correct else "❌ FAIL"
        print(f"Query    : '{q_text}'")
        print(f"Top Hit  : {top_hit_id} (Score: {top_score:.4f})")
        print(f"Expected : {bench['expected_top_id']}")
        print(f"Status   : {status_icon}")
        print("-" * 50)

    accuracy = (hits / total) * 100
    print(f"\n[Phase 12] Final Precision@1 Accuracy: {accuracy:.1f}% ({hits}/{total} queries passed)")

if __name__ == "__main__":
    run_search_evaluation()