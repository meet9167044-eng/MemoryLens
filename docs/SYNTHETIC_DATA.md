# SYNTHETIC DATA

Everything shown in Review 1 must work using synthetic/predefined data.

## Scale
- Review 1 should eventually contain approximately 20–30 high-quality synthetic Memories.
- The architecture must be capable of supporting 60–100 memories seamlessly.

## Content Requirements
- **Realistic sources:** VS Code, Chrome, Terminal, Jupyter, Figma, Slack, PDF Viewer
- **Realistic topics:** CUDA, GPU, PyTorch, Python, Debugging, Web development, UI design, Research, Project planning, DevJams, Documentation, MemoryLens

## Screenshots
Synthetic screenshots must live under: `public/synthetic/screenshots/`
Do not use random unrelated screenshots.

## Required Example Memory
The Review 1 prototype must contain this specific synthetic example:

```json
{
  "id": "mem_1827",
  "timestamp": "2026-01-14T10:32:00",
  "source": {
    "app": "VS Code",
    "type": "desktop"
  },
  "screenshot": {
    "id": "1827",
    "imageUrl": "/synthetic/screenshots/1827.png"
  },
  "content": {
    "ocrText": "RuntimeError: CUDA out of memory...",
    "title": "CUDA Out of Memory Error",
    "summary": "A PyTorch process exceeded available GPU memory."
  },
  "entities": [
    { "id": "entity_cuda", "name": "CUDA", "type": "technology" },
    { "id": "entity_pytorch", "name": "PyTorch", "type": "framework" },
    { "id": "entity_nvidia", "name": "NVIDIA", "type": "company" }
  ],
  "tags": [ "error", "gpu", "python" ],
  "relatedMemories": [
    { "memoryId": "mem_1842", "relationship": "same_topic", "similarityScore": 0.91 },
    { "memoryId": "mem_1809", "relationship": "related_error", "similarityScore": 0.87 }
  ],
  "metadata": {
    "language": "en",
    "contentType": "error",
    "confidence": 0.96
  }
}
```
This represents:
- Screenshot ID: 1827
- Timestamp: January 14, 2026, 10:32 AM
- Source: VS Code
- OCR: "RuntimeError: CUDA out of memory..."
- Entities: CUDA, PyTorch, NVIDIA
- Tags: error, gpu, python
- Related IDs: 1842 and 1809
