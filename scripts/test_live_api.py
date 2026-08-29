import requests
import json

# ──────────────────────────────────────────────────────────
# PHASE 12 — Live API End-to-End Evaluation
# Tests the actual FastAPI backend and PostgreSQL database
# ──────────────────────────────────────────────────────────

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    print("── 1. Testing API Health ───────────────────────────")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Body: {response.json()}\n")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to FastAPI. Is it running on port 8000?")
        return False

def test_live_search(query: str):
    print(f"── 2. Testing Live Search ──────────────────────────")
    print(f"Query: '{query}'")
    
    try:
        # Assuming your Phase 11 teammates created a GET /search endpoint
        response = requests.get(f"{BASE_URL}/search", params={"q": query})
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Success! Found {len(results)} results from the database.")
            print(json.dumps(results, indent=2))
        else:
            print(f"⚠️ Search returned status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Search Error: {e}")

if __name__ == "__main__":
    print("Starting Live API Evaluation...\n")
    if test_health():
        # Let's test one of the queries from your evaluation suite!
        test_live_search("CUDA memory error in PyTorch")