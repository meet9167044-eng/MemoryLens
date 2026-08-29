/**
 * src/services/chatService.ts
 * API client for MemoryLens AI chat endpoints.
 */

import type { VisualChatResponse, ChatResponse } from '../types/chat';

const API_BASE = 'http://localhost:8000/api/v1';

/** POST /api/v1/chat/visual — PaliGemma 2 visual Q&A */
export async function askVisual(
  imageFile: File,
  question: string
): Promise<VisualChatResponse> {
  const form = new FormData();
  form.append('file', imageFile);
  form.append('question', question);

  const res = await fetch(`${API_BASE}/chat/visual`, {
    method: 'POST',
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json() as Promise<VisualChatResponse>;
}

/** POST /api/v1/chat — Gemini RAG text-based chat */
export async function askText(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json() as Promise<ChatResponse>;
}

/** GET /api/v1/health — check if backend is up */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    return res.ok;
  } catch {
    return false;
  }
}
