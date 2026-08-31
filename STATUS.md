# MemoryLens Project Status

## Phase A — Codebase Cleanup ✅ DONE
- [x] Fixed Groq vision model (`llama-3.2-11b-vision-preview`) — this was the root cause of missing tags/summaries
- [x] Fixed Groq chat model (`llama-3.1-8b-instant`)
- [x] Deleted dead backend stub (`backend/main.py`)
- [x] Deleted dead flat frontend pages (`src/pages/Overview.tsx`, `Connections.tsx`, `Memories.tsx`, `Timeline.tsx`, `Insights.tsx`)
- [x] Created `DEVELOPER.md` with full setup guide
- [x] Upgraded Insights API with real stats (confidence avg, success rate, app breakdown)
- [x] Added `file_hash` column to `Screenshot` model for deduplication
- [x] Fixed `file_size_bytes` from `String` to `Integer`
- [x] Added deduplication check in ingest endpoint (prevents re-processing identical files)
- [x] DB migration applied: `2c5f3091dea7_add_file_hash_fix_file_size_bytes`

## Phase B — Timestamps & App Detection ⬜ NEXT
- [ ] Add `app_detected` column to Memory model
- [ ] Extract `captured_at` from EXIF in preprocessing stage
- [ ] Persist `app_detected` from LLM extraction
- [ ] Show `app_detected` in frontend

## Phase C — Real Vector Search ⬜ PENDING
## Phase D — Knowledge Graph Engine ⬜ PENDING
## Phase E — Auto-Ingestion ⬜ PENDING
## Phase F — Scalability ⬜ PENDING
## Phase G — UX Polish ⬜ PENDING
## Phase H — Demo Preparation ⬜ PENDING
## Phase I — Extra Improvements ⬜ PENDING
