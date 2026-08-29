import json
import re
import spacy

# ──────────────────────────────────────────────────────────
# PHASE 6 — MemoryLens Entity + Metadata Extraction
#
# 100% LOCAL. No API key. No internet required.
#
# Uses spaCy (pre-trained NLP model) to extract entities
# from OCR text, then applies MemoryLens-specific rules
# to classify tags, content type, and programming language.
#
# When Member 4 finishes Phase 5 (OCR), replace the
# HARDCODED_OCR_TEXT below with their real OCR output.
# ──────────────────────────────────────────────────────────

# Load the local spaCy English model (runs on your CPU)
print("[Phase 6] Loading local NLP model...")
nlp = spacy.load("en_core_web_sm")
print("[Phase 6] Model loaded successfully!")

# ── HARDCODED OCR TEXT (Replace with Member 4's output later) ──
HARDCODED_OCR_TEXT = """
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from model import SimpleCNN

batch_size = 128
epochs = 10
learning_rate = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Epoch: 1/10
Traceback (most recent call last):
  File "/home/user/mnist_cnn/train.py", line 32, in module
    output = model(data)
RuntimeError: CUDA out of memory. Tried to allocate 1.45 GiB
GPU 0; 8.00 GiB total capacity; 6.32 GiB already allocated
"""

# ── TECHNOLOGY KEYWORD DICTIONARY ─────────────────────────
# These are MemoryLens-specific rules.
# spaCy is great at people/orgs but needs help with tech terms.
# Dictionary maps lowercase keyword → (display name, entity type)
TECH_KEYWORDS = {
    "cuda":             ("CUDA",        "technology"),
    "gpu":              ("GPU",         "technology"),
    "cpu":              ("CPU",         "technology"),
    "docker":           ("Docker",      "technology"),
    "linux":            ("Linux",       "technology"),
    "pytorch":          ("PyTorch",     "framework"),
    "torchvision":      ("TorchVision", "framework"),
    "tensorflow":       ("TensorFlow",  "framework"),
    "react":            ("React",       "framework"),
    "fastapi":          ("FastAPI",     "framework"),
    "numpy":            ("NumPy",       "framework"),
    "pandas":           ("Pandas",      "framework"),
    "python":           ("Python",      "language"),
    "javascript":       ("JavaScript",  "language"),
    "typescript":       ("TypeScript",  "language"),
    "vs code":          ("VS Code",     "tool"),
    "vscode":           ("VS Code",     "tool"),
    "jupyter":          ("Jupyter",     "tool"),
    "github":           ("GitHub",      "tool"),
    "terminal":         ("Terminal",    "tool"),
    "nvidia":           ("NVIDIA",      "company"),
    "google":           ("Google",      "company"),
    "microsoft":        ("Microsoft",   "company"),
}

# ── CONTENT TYPE RULES ─────────────────────────────────────
def detect_content_type(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["traceback", "runtimeerror", "error:", "exception"]):
        return "error"
    if any(w in text_lower for w in ["import", "def ", "class ", "function", "return"]):
        return "code"
    if any(w in text_lower for w in ["http", "www.", ".com", "url", "browser"]):
        return "browser"
    if any(w in text_lower for w in ["$", ">>", "terminal", "bash", "zsh"]):
        return "terminal"
    return "other"

# ── PROGRAMMING LANGUAGE DETECTION ────────────────────────
def detect_language(text: str) -> str:
    text_lower = text.lower()
    if "import torch" in text_lower or "def " in text_lower and "python" not in text_lower:
        return "Python"
    if "import torch" in text_lower or ".py" in text_lower:
        return "Python"
    if "const " in text_lower or "let " in text_lower or ".js" in text_lower:
        return "JavaScript"
    if ".ts" in text_lower or "interface " in text_lower:
        return "TypeScript"
    return None

# ── TAG GENERATOR ──────────────────────────────────────────
def generate_tags(text: str, entities: list) -> list:
    tags = set()
    text_lower = text.lower()

    # Only add meaningful predefined tags — no numbers, no noise
    if any(w in text_lower for w in ["error", "traceback", "exception", "failed"]):
        tags.add("error")
    if any(w in text_lower for w in ["gpu", "cuda", "nvidia", "memory"]):
        tags.add("gpu")
    if any(w in text_lower for w in ["python", ".py", "import torch"]):
        tags.add("python")
    if "pytorch" in text_lower or "torch" in text_lower:
        tags.add("pytorch")
    if "cuda" in text_lower:
        tags.add("cuda")
    if "training" in text_lower or "epoch" in text_lower:
        tags.add("training")
    if "memory" in text_lower:
        tags.add("memory")

    return sorted(list(tags))

# ── TITLE GENERATOR ───────────────────────────────────────
def generate_title(content_type: str, entities: list, text: str) -> str:
    # Extract the first error line if present
    for line in text.split("\n"):
        line = line.strip()
        if "Error:" in line or "Error" in line and len(line) < 80:
            return line[:60]  # cap at 60 chars

    entity_names = [e["name"] for e in entities[:2]]
    if entity_names:
        return f"{' + '.join(entity_names)} — {content_type.capitalize()} Screenshot"

    return f"Screenshot — {content_type.capitalize()}"

# ── SUMMARY GENERATOR ─────────────────────────────────────
def generate_summary(content_type: str, entities: list, tags: list) -> str:
    entity_names = [e["name"] for e in entities[:3]]
    if content_type == "error" and entity_names:
        return f"A {entity_names[0]} error occurred involving {', '.join(entity_names[1:])}."
    if entity_names:
        return f"Screenshot involves {', '.join(entity_names)}."
    return "Screenshot captured from digital activity."

# ── MAIN EXTRACTION FUNCTION ──────────────────────────────
def extract_metadata(ocr_text: str) -> dict:
    """
    PHASE 6 — MemoryLens Metadata + Entity Extraction

    Takes raw OCR text and returns a fully structured
    metadata dictionary ready to be saved into the database.

    Args:
        ocr_text : Raw OCR text from Phase 5

    Returns:
        Structured metadata dictionary
    """

    result = {
        "title": None,
        "summary": None,
        "app": None,
        "content_type": None,
        "language": None,
        "entities": [],
        "tags": [],
        "success": False,
        "error": None
    }

    try:
        text_lower = ocr_text.lower()

        # ── STEP 1: Detect Content Type ───────────────────
        result["content_type"] = detect_content_type(ocr_text)
        print(f"[Phase 6] Content type: {result['content_type']}")

        # ── STEP 2: Detect Programming Language ───────────
        result["language"] = detect_language(ocr_text)
        print(f"[Phase 6] Language: {result['language']}")

        # ── STEP 3: Extract Entities using spaCy ──────────
        doc = nlp(ocr_text)
        entities = []
        seen = set()

                # spaCy named entities (ORG, PERSON, GPE, etc.)
        # Filter out: numbers, short strings, and numeric-looking strings
        for ent in doc.ents:
            name = ent.text.strip()
            # Skip if it's a number, too short, or looks like a float/fraction
            if len(name) <= 2:
                continue
            if re.match(r'^[\d\.\/:]+$', name):
                continue
            if name not in seen:
                entities.append({
                    "name": name,
                    "type": "other",
                    "source": "spacy"
                })
                seen.add(name)

        # MemoryLens tech keyword rules
                # MemoryLens tech keyword rules
        for keyword, (display_name, entity_type) in TECH_KEYWORDS.items():
            if keyword in text_lower and display_name not in seen:
                entities.append({
                    "name": display_name,
                    "type": entity_type,
                    "source": "keyword_rule"
                })
                seen.add(display_name)

        result["entities"] = entities
        print(f"[Phase 6] Entities found: {[e['name'] for e in entities]}")

        # ── STEP 4: Generate Tags ──────────────────────────
        result["tags"] = generate_tags(ocr_text, entities)
        print(f"[Phase 6] Tags: {result['tags']}")

        # ── STEP 5: Detect App ────────────────────────────
        if "vs code" in text_lower or "visual studio code" in text_lower:
            result["app"] = "VS Code"
        elif "terminal" in text_lower or "$" in ocr_text:
            result["app"] = "Terminal"
        elif "chrome" in text_lower or "http" in text_lower:
            result["app"] = "Chrome"
        elif "jupyter" in text_lower:
            result["app"] = "Jupyter"
        else:
            result["app"] = "Unknown"
        print(f"[Phase 6] App: {result['app']}")

        # ── STEP 6: Generate Title + Summary ──────────────
        result["title"] = generate_title(
            result["content_type"], entities, ocr_text
        )
        result["summary"] = generate_summary(
            result["content_type"], entities, result["tags"]
        )

        result["success"] = True
        print("[Phase 6] ✅ Extraction complete!")

    except Exception as e:
        result["error"] = str(e)
        print(f"[Phase 6] ❌ Error: {e}")

    return result


# ── RUN TEST ──────────────────────────────────────────────
if __name__ == "__main__":
    print("── Phase 6: Entity + Metadata Extraction ───────────")
    print("Using hardcoded OCR text (swap with Member 4 output later)\n")

    result = extract_metadata(HARDCODED_OCR_TEXT)

    print("\n── FINAL RESULT ─────────────────────────────────────")
    print(json.dumps(result, indent=2))