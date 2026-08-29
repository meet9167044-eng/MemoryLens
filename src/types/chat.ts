/**
 * src/types/chat.ts
 * TypeScript types for the MemoryLens AI Chat API.
 */

/** Response from POST /api/v1/chat/visual (PaliGemma 2 visual Q&A) */
export type VisualChatResponse = {
  question: string;
  answer: string;
  model: string;
  backend: 'colab_proxy' | 'local_gpu' | 'unavailable';
};

/** A memory citation returned by the text RAG chat */
export type Citation = {
  memory_id: string;
  title: string;
  timestamp: string;
  snippet: string;
};

/** Response from POST /api/v1/chat (Gemini RAG text chat) */
export type ChatResponse = {
  answer: string;
  citations: Citation[];
  memories_searched: number;
  model_used: string;
};

/** A single message in the chat UI */
export type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  imageUrl?: string;      // data URL shown in UI for uploaded images
  citations?: Citation[];
  model?: string;
  backend?: string;
  timestamp: Date;
  isLoading?: boolean;
};
