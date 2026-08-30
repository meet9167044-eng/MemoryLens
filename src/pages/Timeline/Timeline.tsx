import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { format } from "date-fns"
import { api, Memory } from "@/services/api"
import { Clock, Monitor } from "lucide-react"

// imageUrl from backend is relative (/api/v1/screenshots/…/image) — Vite proxy handles it

export default function Timeline() {
  const [timelineItems, setTimelineItems] = useState<Memory[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    api.getTimeline({ limit: 100 }).then(data => {
      setTimelineItems(data || [])
      setLoading(false)
    })
  }, [])

  const grouped = timelineItems.reduce((acc, item) => {
    const d = format(new Date(item.timestamp || new Date()), "MMMM d, yyyy")
    if (!acc[d]) acc[d] = []
    acc[d].push(item)
    return acc
  }, {} as Record<string, Memory[]>)

  return (
    <div style={{ maxWidth: '860px', margin: '0 auto' }}>
      <div className="page-header">
        <div>
          <h1 className="page-title letterpress">Timeline</h1>
          <p className="page-subtitle">Your digital activity across time, in chronological order.</p>
        </div>
      </div>

      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
          {[1, 2].map(i => (
            <div key={i}>
              <div className="skeleton" style={{ height: '28px', width: '200px', marginBottom: '20px' }}></div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', paddingLeft: '40px' }}>
                {[1, 2].map(j => <div key={j} className="skeleton" style={{ height: '100px' }}></div>)}
              </div>
            </div>
          ))}
        </div>
      ) : Object.keys(grouped).length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '48px' }}>
          {Object.entries(grouped).map(([date, mems]) => (
            <div key={date} className="timeline-section">
              <div className="timeline-date">{date}</div>
              <div className="timeline-list">
                {mems.map((memory) => (
                  <div key={memory.id} className="timeline-item" onClick={() => navigate(`/memories/${memory.id}`)}>
                    <div className="timeline-dot"></div>
                    <div className="memory-card-row">
                      {memory.screenshot?.imageUrl && (
                        <div className="memory-card-thumb" style={{ width: '120px', minHeight: '90px' }}>
                          <img
                            src={memory.screenshot.imageUrl}
                            alt=""
                            onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
                          />
                        </div>
                      )}
                      <div className="memory-card-body">
                        <div className="memory-card-meta">
                          <Clock size={12} />
                          <span>{format(new Date(memory.timestamp || new Date()), "h:mm a")}</span>
                          <span>•</span>
                          <span style={{ color: 'var(--accent)', fontWeight: 600 }}>
                            <Monitor size={12} style={{ display: 'inline', marginRight: '3px' }} />
                            {memory.source?.app || 'Unknown'}
                          </span>
                        </div>
                        <div className="memory-card-title">{memory.content?.title || 'Untitled'}</div>
                        <div className="memory-card-summary">{memory.content?.summary}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state" style={{ height: '50vh' }}>
          <div className="empty-icon"><Clock size={28} /></div>
          <div className="empty-title">No timeline events</div>
          <p>Capture some memories to build your timeline.</p>
        </div>
      )}
    </div>
  )
}
