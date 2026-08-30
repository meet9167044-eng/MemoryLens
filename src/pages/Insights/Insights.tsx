import { useEffect, useState } from "react"
import { api, InsightStats } from "@/services/api"
import { BarChart3, TrendingUp, Zap, FileText, Share2 } from "lucide-react"

export default function Insights() {
  const [insights, setInsights] = useState<InsightStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      const stats = await api.getInsights()
      setInsights(stats)
      setLoading(false)
    }
    fetchData()
  }, [])

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title letterpress">System Insights</h1>
          <p className="page-subtitle">Analytics on your digital memory capture and processing pipeline.</p>
        </div>
        <div className="live-indicator">
          <div className="live-dot"></div>
          Live Processing
        </div>
      </div>

      {loading ? (
        <div className="stats-row">
          {[1, 2, 3].map(i => (
            <div key={i} className="skeleton" style={{ height: '140px' }}></div>
          ))}
        </div>
      ) : (
        <>
          <div className="stats-row">
            <div className="stat-card">
              <div className="stat-label"><FileText size={14} /> Total Captured</div>
              <div className="stat-value">{insights?.total_memories || 0}</div>
              <div className="stat-sub"><TrendingUp size={13} /> +12% from last week</div>
            </div>
            <div className="stat-card">
              <div className="stat-label"><Share2 size={14} /> Entities Extracted</div>
              <div className="stat-value">{insights?.total_entities || 0}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--secondary-text)', marginTop: '8px' }}>Across multiple categories</div>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #EFF6FF 0%, #fff 100%)', borderColor: '#DBEAFE' }}>
              <div className="stat-label" style={{ color: '#1D4ED8' }}><Zap size={14} /> OCR Confidence</div>
              <div className="stat-value" style={{ color: '#1e40af' }}>98.2%</div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: '98.2%' }}></div>
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '8px' }}>
            <div className="card">
              <div className="card-header">
                <div className="card-title">Top Semantic Tags</div>
                <div className="card-desc">Most frequently detected topics across all memories.</div>
              </div>
              <div className="card-content">
                {insights?.top_tags?.length ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                    {insights.top_tags.map((tag, i) => (
                      <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <span style={{ color: '#9CA3AF', fontFamily: 'monospace', fontSize: '0.8rem', width: '16px' }}>{i + 1}</span>
                          <span style={{ fontWeight: 500, fontSize: '0.9rem' }}>{tag.name}</span>
                        </div>
                        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--secondary-text)' }}>{tag.count}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ textAlign: 'center', padding: '24px', color: 'var(--secondary-text)', fontSize: '0.875rem' }}>
                    No tag data available yet.
                  </div>
                )}
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <div className="card-title">Pipeline Activity</div>
                <div className="card-desc">Processing throughput over the last 7 days.</div>
              </div>
              <div className="card-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '200px', flexDirection: 'column', color: '#9CA3AF' }}>
                <BarChart3 size={48} strokeWidth={1} style={{ marginBottom: '12px', opacity: 0.4 }} />
                <span style={{ fontSize: '0.85rem' }}>Chart will populate with real data</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
