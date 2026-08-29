# PRODUCT: MemoryLens Review 1

## Overview
The application should feel like a professional developer productivity/productivity-memory tool. It should NOT look like a flashy AI demo.

## User State
There is currently no authentication. The default user is "Virat". 
The Overview greeting should always be: **"Good morning, Virat."** (Do NOT use "Good morning, DevJams.")

## Primary Navigation and Screens

### 1. Overview
Provides a quick understanding of the user's digital memory activity.
- **Content:** Greeting, recent memories, recent topics, simple activity summary.
- **Goal:** Keep it minimal. Do not overload the dashboard with charts.

### 2. Memories
The main browsing screen.
- **Content:** Memory cards showing title, source, timestamp, summary, tags.
- **Behavior:** Cards should be clickable and lead to Memory Detail.

### 3. Memory Detail
One of the most important screens for Review 1.
- **Information Hierarchy:** Evidence ↓ Understanding ↓ Classification ↓ Relationships
- **Content:** title, source, timestamp, screenshot (original evidence), summary, OCR text, entities, tags, related memories.

### 4. Search
Operates only on the synthetic dataset.
- **Behavior:** Simple local string matching is sufficient for Review 1. Do NOT implement real semantic/vector search.
- **Searchable fields:** title, OCR text, tags, entities, summary.

### 5. Timeline
Displays Memories chronologically.
- **Behavior:** Items grouped by date/time and clickable.

### 6. Connections
Shows relationships between Memories, Entities, and Topics.
- **Behavior:** A simple visual relationship representation is sufficient. Do not over-engineer graph infrastructure.

### 7. Insights
Shows predefined synthetic patterns (e.g., "GPU debugging: 12 memories").
- **Constraint:** These are synthetic observations. Do not claim that a real AI system generated them.
