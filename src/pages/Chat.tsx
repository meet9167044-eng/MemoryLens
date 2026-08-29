import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Sparkles, Send, ImagePlus, X, Bot, User,
  Zap, Server, CheckCircle, AlertCircle, Loader2,
} from 'lucide-react';
import { askVisual, askText, checkBackendHealth } from '../services/chatService';
import type { ChatMessage } from '../types/chat';

// ─── Preset questions tied to hackathon photos ────────────────────────────────
const PRESETS = [
  { label: '👜 Tote bag quote', q: 'What quote is written on the tote bag?' },
  { label: '💧 Water bottle', q: 'Where is my water bottle and what does it say?' },
  { label: '👓 Round spectacles', q: 'Where are my round spectacles?' },
  { label: '🍌 Snacks on desk', q: 'What snacks do we have on the table?' },
  { label: '💻 Who has a laptop?', q: 'Who was working on a laptop at the table?' },
  { label: '🏟️ Hall description', q: 'Describe the hackathon hall environment.' },
];

// ─── Tiny ID helper ───────────────────────────────────────────────────────────
const uid = () => Math.random().toString(36).slice(2, 9);

// ─── Component ────────────────────────────────────────────────────────────────
export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: uid(),
      role: 'assistant',
      text: "Hello! I'm your **MemoryLens AI**, powered by a fine-tuned PaliGemma 2 model trained on your real hackathon memories.\n\nUpload any photo and ask me a question — or just type a text question to search your memory index!",
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth().then(setBackendOnline);
  }, []);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // ── File selection ──────────────────────────────────────────────────────────
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    setSelectedFile(file);
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // ── Send message ────────────────────────────────────────────────────────────
  const sendMessage = useCallback(async (questionOverride?: string) => {
    const question = (questionOverride ?? inputText).trim();
    if (!question) return;
    if (isLoading) return;

    const userMsg: ChatMessage = {
      id: uid(),
      role: 'user',
      text: question,
      imageUrl: previewUrl ?? undefined,
      timestamp: new Date(),
    };

    const loadingMsg: ChatMessage = {
      id: uid(),
      role: 'assistant',
      text: '',
      timestamp: new Date(),
      isLoading: true,
    };

    setMessages(prev => [...prev, userMsg, loadingMsg]);
    setInputText('');
    setIsLoading(true);

    // Keep file reference before clearing
    const fileToSend = selectedFile;
    clearFile();

    try {
      let result: ChatMessage;

      if (fileToSend) {
        // Visual Q&A via PaliGemma 2
        const res = await askVisual(fileToSend, question);
        result = {
          id: loadingMsg.id,
          role: 'assistant',
          text: res.answer,
          model: res.model,
          backend: res.backend,
          timestamp: new Date(),
        };
      } else {
        // Text RAG via Gemini
        const res = await askText(question);
        result = {
          id: loadingMsg.id,
          role: 'assistant',
          text: res.answer,
          citations: res.citations,
          model: res.model_used,
          backend: 'rag',
          timestamp: new Date(),
        };
      }

      setMessages(prev =>
        prev.map(m => (m.id === loadingMsg.id ? result : m))
      );
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : 'Unknown error';
      setMessages(prev =>
        prev.map(m =>
          m.id === loadingMsg.id
            ? {
                ...m,
                text: `⚠️ **Error:** ${errMsg}\n\nMake sure the backend server is running at \`localhost:8000\` and your Colab session is active.`,
                isLoading: false,
              }
            : m
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, [inputText, selectedFile, previewUrl, isLoading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <div style={styles.page}>
      {/* ── Header ── */}
      <div style={styles.header}>
        <div style={styles.headerLeft}>
          <div style={styles.logoBox}>
            <Sparkles size={20} color="#fff" />
          </div>
          <div>
            <h1 style={styles.title}>Ask MemoryLens AI</h1>
            <p style={styles.subtitle}>
              Powered by fine-tuned <strong>PaliGemma 2</strong> (3B · LoRA) + Gemini RAG
            </p>
          </div>
        </div>

        {/* Backend status */}
        <div style={styles.statusPill}>
          <Server size={14} />
          {backendOnline === null ? (
            <span style={{ color: '#9ca3af' }}>Checking…</span>
          ) : backendOnline ? (
            <>
              <CheckCircle size={14} color="#34d399" />
              <span style={{ color: '#34d399' }}>Backend Online</span>
            </>
          ) : (
            <>
              <AlertCircle size={14} color="#f87171" />
              <span style={{ color: '#f87171' }}>Backend Offline</span>
            </>
          )}
        </div>
      </div>

      {/* ── Preset chips ── */}
      <div style={styles.presetsRow}>
        <Zap size={13} color="#fbbf24" />
        <span style={styles.presetsLabel}>Quick questions:</span>
        {PRESETS.map(p => (
          <button
            key={p.q}
            style={styles.presetChip}
            onClick={() => sendMessage(p.q)}
            disabled={isLoading}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* ── Chat area ── */}
      <div style={styles.chatArea}>
        {messages.map(msg => (
          <MessageBubble key={msg.id} msg={msg} />
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* ── Image preview ── */}
      {previewUrl && (
        <div style={styles.previewBar}>
          <img src={previewUrl} alt="Selected" style={styles.previewImg} />
          <span style={styles.previewName}>{selectedFile?.name}</span>
          <button style={styles.previewRemove} onClick={clearFile}>
            <X size={14} />
          </button>
        </div>
      )}

      {/* ── Input area ── */}
      <div style={styles.inputRow}>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
        <button
          style={styles.attachBtn}
          onClick={() => fileInputRef.current?.click()}
          title="Upload an image"
        >
          <ImagePlus size={18} color={selectedFile ? '#818cf8' : '#6b7280'} />
        </button>
        <textarea
          style={styles.textInput}
          placeholder={
            selectedFile
              ? 'Ask a question about the image…'
              : 'Ask anything, or upload an image to use PaliGemma 2 visual recall…'
          }
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />
        <button
          style={{
            ...styles.sendBtn,
            opacity: isLoading || !inputText.trim() ? 0.5 : 1,
          }}
          onClick={() => sendMessage()}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? (
            <Loader2 size={18} color="#fff" style={{ animation: 'spin 1s linear infinite' }} />
          ) : (
            <Send size={18} color="#fff" />
          )}
        </button>
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
      `}</style>
    </div>
  );
};

// ─── Message bubble sub-component ─────────────────────────────────────────────
function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === 'user';

  return (
    <div style={{ ...styles.msgRow, justifyContent: isUser ? 'flex-end' : 'flex-start', animation: 'fadeIn 0.25s ease' }}>
      {!isUser && (
        <div style={styles.avatarBot}>
          <Sparkles size={14} color="#818cf8" />
        </div>
      )}

      <div style={{ maxWidth: '72%' }}>
        {/* Image preview in user bubble */}
        {msg.imageUrl && (
          <img
            src={msg.imageUrl}
            alt="Uploaded"
            style={{
              ...styles.msgImage,
              marginLeft: isUser ? 'auto' : '0',
            }}
          />
        )}

        <div
          style={{
            ...styles.bubble,
            ...(isUser ? styles.bubbleUser : styles.bubbleBot),
          }}
        >
          {msg.isLoading ? (
            <div style={styles.loadingDots}>
              <span>●</span><span>●</span><span>●</span>
            </div>
          ) : (
            <span style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
              {msg.text.replace(/\*\*(.*?)\*\*/g, '$1')}
            </span>
          )}
        </div>

        {/* Model badge */}
        {!isUser && msg.model && !msg.isLoading && (
          <div style={styles.modelBadge}>
            <Bot size={11} />
            {msg.backend === 'colab_proxy'
              ? `PaliGemma 2 · LoRA (Colab GPU)`
              : msg.backend === 'local_gpu'
              ? `PaliGemma 2 · LoRA (Local GPU)`
              : msg.backend === 'rag'
              ? `Gemini RAG · ${msg.citations?.length ?? 0} citations`
              : msg.model}
          </div>
        )}

        {/* Citations */}
        {msg.citations && msg.citations.length > 0 && (
          <div style={styles.citations}>
            <span style={styles.citationsLabel}>📎 Sources:</span>
            {msg.citations.map(c => (
              <div key={c.memory_id} style={styles.citation}>
                <strong>{c.title}</strong> — {c.snippet}
              </div>
            ))}
          </div>
        )}
      </div>

      {isUser && (
        <div style={styles.avatarUser}>
          <User size={14} color="#818cf8" />
        </div>
      )}
    </div>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────
const styles: Record<string, React.CSSProperties> = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    maxWidth: 900,
    margin: '0 auto',
    padding: '24px 24px 0',
    gap: 16,
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: '#f1f5f9',
    boxSizing: 'border-box',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: 12,
  },
  headerLeft: { display: 'flex', alignItems: 'center', gap: 12 },
  logoBox: {
    width: 40, height: 40, borderRadius: 12,
    background: 'linear-gradient(135deg, #6366f1, #06b6d4)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 0 20px rgba(99,102,241,0.4)',
  },
  title: { fontSize: 20, fontWeight: 700, margin: 0, color: '#f8fafc' },
  subtitle: { fontSize: 12, color: '#94a3b8', margin: '2px 0 0' },
  statusPill: {
    display: 'flex', alignItems: 'center', gap: 6,
    background: 'rgba(15,23,42,0.8)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 20, padding: '6px 14px', fontSize: 12, color: '#94a3b8',
  },
  presetsRow: {
    display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 8,
    background: 'rgba(15,23,42,0.6)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: 12, padding: '10px 16px',
  },
  presetsLabel: { fontSize: 12, color: '#94a3b8', marginRight: 4 },
  presetChip: {
    fontSize: 12, padding: '4px 12px', borderRadius: 20,
    background: 'rgba(30,41,59,0.8)',
    border: '1px solid rgba(99,102,241,0.3)',
    color: '#c7d2fe', cursor: 'pointer',
    transition: 'all 0.15s',
  },
  chatArea: {
    flex: 1, overflowY: 'auto', display: 'flex',
    flexDirection: 'column', gap: 16,
    paddingRight: 4, paddingBottom: 8,
    minHeight: 300,
  },
  msgRow: { display: 'flex', alignItems: 'flex-end', gap: 10 },
  avatarBot: {
    width: 32, height: 32, borderRadius: 10, flexShrink: 0,
    background: 'rgba(99,102,241,0.15)',
    border: '1px solid rgba(99,102,241,0.4)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  avatarUser: {
    width: 32, height: 32, borderRadius: 10, flexShrink: 0,
    background: 'rgba(99,102,241,0.2)',
    border: '1px solid rgba(99,102,241,0.5)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  bubble: {
    padding: '12px 16px', borderRadius: 16, fontSize: 14,
    lineHeight: 1.6, wordBreak: 'break-word',
  },
  bubbleUser: {
    background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
    borderBottomRightRadius: 4, color: '#fff',
    boxShadow: '0 4px 20px rgba(99,102,241,0.3)',
  },
  bubbleBot: {
    background: 'rgba(21,29,48,0.85)',
    border: '1px solid rgba(255,255,255,0.09)',
    borderBottomLeftRadius: 4, color: '#e2e8f0',
  },
  msgImage: {
    width: '100%', maxHeight: 200, objectFit: 'cover',
    borderRadius: 12, marginBottom: 8,
    border: '1px solid rgba(255,255,255,0.1)',
  },
  modelBadge: {
    display: 'flex', alignItems: 'center', gap: 5,
    fontSize: 11, color: '#64748b', marginTop: 6,
  },
  citations: {
    marginTop: 8, padding: '8px 12px',
    background: 'rgba(15,23,42,0.6)',
    border: '1px solid rgba(99,102,241,0.2)',
    borderRadius: 10, fontSize: 12,
  },
  citationsLabel: { fontWeight: 600, color: '#94a3b8', display: 'block', marginBottom: 4 },
  citation: { color: '#cbd5e1', marginTop: 4, lineHeight: 1.5 },
  loadingDots: {
    display: 'flex', gap: 6,
    '& span': { animation: 'pulse 1s ease-in-out infinite' },
  },
  previewBar: {
    display: 'flex', alignItems: 'center', gap: 10,
    background: 'rgba(21,29,48,0.8)',
    border: '1px solid rgba(99,102,241,0.4)',
    borderRadius: 12, padding: '8px 12px',
  },
  previewImg: { height: 40, width: 40, objectFit: 'cover', borderRadius: 8 },
  previewName: { flex: 1, fontSize: 12, color: '#94a3b8', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' },
  previewRemove: {
    background: 'transparent', border: 'none', cursor: 'pointer',
    color: '#6b7280', padding: 4, display: 'flex', alignItems: 'center',
  },
  inputRow: {
    display: 'flex', alignItems: 'flex-end', gap: 10,
    background: 'rgba(15,23,42,0.8)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 16, padding: '10px 14px',
    marginBottom: 16,
  },
  attachBtn: {
    background: 'transparent', border: 'none',
    cursor: 'pointer', padding: 4,
    display: 'flex', alignItems: 'center',
  },
  textInput: {
    flex: 1, background: 'transparent', border: 'none',
    color: '#f1f5f9', fontSize: 14, resize: 'none',
    outline: 'none', lineHeight: 1.5, fontFamily: 'inherit',
    minHeight: 24, maxHeight: 120,
  },
  sendBtn: {
    background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
    border: 'none', borderRadius: 10,
    width: 36, height: 36,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    cursor: 'pointer', flexShrink: 0,
    boxShadow: '0 4px 12px rgba(99,102,241,0.4)',
  },
};
