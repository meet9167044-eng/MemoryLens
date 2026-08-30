import React, { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { format } from "date-fns"
import { api, Memory, RelatedMemoryFull } from "@/services/api"
import { ArrowLeft, Clock, Monitor, Tag, AlignLeft, Layers, Network } from "lucide-react"

export default function MemoryDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [memory, setMemory] = useState<Memory | null>(null)
  const [related, setRelated] = useState<RelatedMemoryFull[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    Promise.all([
      api.getMemory(id),
      api.getRelatedMemories(id)
    ]).then(([mem, rel]) => {
      setMemory(mem)
      setRelated(rel?.related || [])
      setLoading(false)
    })
  }, [id])

  if (loading) {
    return (
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <div className="skeleton" style={{ height: '32px', width: '80px', marginBottom: '24px' }}></div>
        <div className="skeleton" style={{ height: '48px', width: '70%', marginBottom: '16px' }}></div>
        <div className="skeleton" style={{ height: '400px', borderRadius: '12px', marginTop: '32px' }}></div>
      </div>
    )
  }

  if (!memory) {
    return (
      <div className="empty-state" style={{ height: '60vh' }}>
        <div className="empty-icon"><Layers size={28} /></div>
        <div className="empty-title">Memory not found</div>
        <button className="btn btn-secondary" style={{ marginTop: '16px' }} onClick={() => navigate("/memories")}>
          Return to Memories
        </button>
      </div>
    )
  }

  // The screenshot imageUrl from backend is a relative path like /api/v1/screenshots/{id}/image
  // With Vite proxy, this works directly as a relative URL.
  const imgUrl = memory.screenshot?.imageUrl || null

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', paddingBottom: '80px' }}>
      <button className="back-btn" onClick={() => navigate(-1)}>
        <ArrowLeft size={16} />
        Back
      </button>

      {/* Title */}
      <div style={{ marginBottom: '36px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '0.8rem', color: 'var(--secondary-text)', marginBottom: '12px', flexWrap: 'wrap' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Clock size={14} />
            {format(new Date(memory.timestamp || new Date()), "MMMM d, yyyy 'at' h:mm a")}
          </span>
          <span>•</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Monitor size={14} /> {memory.source?.app || 'Unknown App'}
          </span>
          <span>•</span>
          <span className={`badge badge-${memory.metadata?.confidence > 0.9 ? 'success' : 'outline'}`}>
            {Math.round((memory.metadata?.confidence || 0) * 100)}% confidence
          </span>
        </div>
        <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: '2.2rem', fontWeight: 700, color: 'var(--primary-text)', lineHeight: 1.2, letterSpacing: '-0.02em', marginBottom: '12px' }}>
          {memory.content?.title || 'Untitled Memory'}
        </h1>
        <p style={{ fontSize: '1rem', color: 'var(--secondary-text)', lineHeight: 1.7, maxWidth: '680px' }}>
          {memory.content?.summary}
        </p>
      </div>

      {/* Detail grid */}
      <div className="detail-grid">
        {/* Left: evidence + OCR */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Monitor size={17} color="var(--accent)" />
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: '1.1rem', fontWeight: 600 }}>Evidence</span>
            </div>
            <div className="detail-evidence">
              {imgUrl ? (
                <img
                  src={imgUrl}
                  alt={memory.content?.title}
                  onError={e => { (e.target as HTMLImageElement).src = ''; (e.target as HTMLImageElement).style.display = 'none' }}
                />
              ) : (
                <div className="empty-state" style={{ height: '200px' }}>
                  <Layers size={36} color="#D1D5DB" />
                  <p style={{ marginTop: '8px', fontSize: '0.875rem' }}>No screenshot available</p>
                </div>
              )}
            </div>
          </div>

          {memory.content?.ocrText && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <AlignLeft size={17} color="var(--accent)" />
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '1.1rem', fontWeight: 600 }}>Captured Text</span>
              </div>
              <div className="detail-ocr">
                <pre>{memory.content.ocrText}</pre>
              </div>
            </div>
          )}
        </div>

        {/* Right: metadata */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Tags */}
          <div className="card">
            <div className="card-header">
              <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Tag size={16} color="var(--accent)" />
                Metadata
              </div>
            </div>
            <div className="card-content">
              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--secondary-text)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '10px' }}>Tags</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {memory.tags?.length
                    ? memory.tags.map((tag, i) => <span key={i} className="badge badge-secondary">#{tag}</span>)
                    : <span style={{ fontSize: '0.85rem', color: 'var(--secondary-text)' }}>No tags</span>
                  }
                </div>
              </div>
              <div style={{ borderTop: '1px solid var(--border)', paddingTop: '16px' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--secondary-text)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '10px' }}>Source Type</div>
                <span className="badge badge-accent">{memory.metadata?.contentType || 'screenshot'}</span>
              </div>
            </div>
          </div>

          {/* Entities */}
          <div className="card">
            <div className="card-header">
              <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Tag size={16} color="var(--accent)" />
                Identified Entities
              </div>
            </div>
            <div className="card-content">
              {memory.entities?.length ? (
                <div>
                  {memory.entities.map((ent, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: i < memory.entities.length - 1 ? '1px solid var(--border)' : 'none' }}>
                      <span style={{ fontWeight: 500, fontSize: '0.875rem' }}>{ent.name}</span>
                      <span className="badge badge-outline" style={{ fontSize: '0.7rem' }}>{ent.type}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <span style={{ fontSize: '0.875rem', color: 'var(--secondary-text)' }}>No entities detected</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Related Memories */}
      {related.length > 0 && (
        <div style={{ marginTop: '48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <Network size={18} color="var(--accent)" />
            <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 600, color: 'var(--primary-text)' }}>
              Related Memories
            </h2>
            <span className="badge badge-outline">{related.length}</span>
          </div>
          <div className="memory-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))' }}>
            {related.map((rel, i) => (
              <div
                key={i}
                className="memory-card-grid"
                onClick={() => navigate(`/memories/${rel.memory_id}`)}
              >
                <div className="memory-card-grid-body" style={{ padding: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    {/* Backend returns rel_type (e.g. "shared_entity", "shared_tag") */}
                    <span className="badge badge-accent" style={{ fontSize: '0.65rem' }}>
                      {(rel.rel_type || '').replace(/_/g, ' ')}
                    </span>
                    {rel.score > 0 && (
                      <span style={{ fontSize: '0.7rem', color: 'var(--secondary-text)', fontWeight: 600 }}>
                        {Math.round(rel.score * 100)}%
                      </span>
                    )}
                  </div>
                  <div style={{ fontWeight: 600, fontSize: '0.875rem', marginBottom: '6px', lineHeight: 1.4 }}>
                    {rel.title || 'Untitled'}
                  </div>
                  {/* Optional summary from enriched backend */}
                  {rel.summary && (
                    <div style={{ fontSize: '0.78rem', color: 'var(--secondary-text)', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {rel.summary}
                    </div>
                  )}
                  {/* explanation fallback */}
                  {!rel.summary && rel.explanation && (
                    <div style={{ fontSize: '0.72rem', color: 'var(--secondary-text)', lineHeight: 1.4, fontStyle: 'italic' }}>
                      {rel.explanation}
                    </div>
                  )}
                  {/* Optional timestamp */}
                  {rel.timestamp && (
                    <div style={{ marginTop: '8px', fontSize: '0.7rem', color: '#9CA3AF' }}>
                      {format(new Date(rel.timestamp), "MMM d, yyyy")}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
