# MemoryLens Project Status

## Phase A — Codebase Cleanup ✅ DONE
- [x] Fixed Groq vision model (`llama-3.2-11b-vision-preview`) — root cause of missing tags/summaries
- [x] Fixed Groq chat model (`llama-3.1-8b-instant`)
- [x] Deleted dead backend stub (`backend/main.py`)
- [x] Deleted dead flat frontend pages
- [x] Created `DEVELOPER.md`
- [x] Upgraded Insights API with real stats
- [x] Added `file_hash` column + deduplication at ingest
- [x] Fixed `file_size_bytes` from `String` to `Integer`
- [x] DB migration applied: `2c5f3091dea7`

## Phase B — Timestamps & App Detection ✅ DONE
- [x] Added `app_detected`, `captured_at`, `domain` columns to `Memory` model
- [x] DB migration applied: `2c766c3a59a7`
- [x] Pipeline `_preprocess()` extracts `captured_at` from EXIF → filename pattern → mtime
- [x] Pipeline `_ai_extraction()` persists `app_detected` from LLM result
- [x] Search results use `app_detected` (not hardcoded "Unknown") and `captured_at` (not upload time)
- [x] Memories API sorts by `captured_at` desc for correct chronological ordering
- [x] Frontend `InsightStats` type updated with new fields

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
