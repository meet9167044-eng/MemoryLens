# Architecture Rules

- The repository already has an established structure. Respect it.
- Do NOT replace the current architecture with a completely different one.
- **Directory Structure:**
  `src/`
  ├── `app/`
  ├── `components/`
  ├── `data/`
  ├── `hooks/`
  ├── `lib/`
  └── `pages/`

## Future Backend Compatibility
Even though Review 1 is frontend-only, design the frontend so that:
`components`
↓
`data/service layer`
↓
`Memory objects`

can later become:
`components`
↓
`data/service/API layer`
↓
`backend`
↓
`database / AI / embeddings`

- Do NOT build the backend now.
- Do NOT create fake API infrastructure just for the sake of architecture.
- The synthetic data source should be replaceable later.
