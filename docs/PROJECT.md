# PROJECT: MemoryLens

## Goal
MemoryLens is a digital-memory interface.
The core concept is:
Capture digital activity → understand it → structure it as a Memory → connect related Memories → allow the user to retrieve and explore them.

## Review 1 Scope
For DevJams Review 1, we are building ONLY the frontend prototype.
- The prototype must demonstrate the core user experience and flow.
- Everything shown in Review 1 must work using synthetic/predefined data.

## Explicitly OUT OF SCOPE for Review 1
- NO backend
- NO authentication (Do NOT create login/signup/profile/logout functionality)
- NO real AI processing
- NO real OCR
- NO database
- NO vector database
- NO real screenshot monitoring
- NO fake API infrastructure just for the sake of architecture

## Future Backend Compatibility
Even though Review 1 is frontend-only, the frontend must be architected cleanly so that a future backend can replace the synthetic data source without requiring a major redesign.
The architecture flow should be:
`components` → `data/service layer` → `Memory objects`
This ensures that the data/service layer can later become an API client connected to a real backend.
