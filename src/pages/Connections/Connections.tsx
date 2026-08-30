import React, { useEffect, useState } from "react"
import { api, GraphNode, GraphEdge } from "@/services/api"
import { Network, Link2, Monitor, Code, Tag, Cpu } from "lucide-react"

type ConnectionsData = { nodes: GraphNode[]; edges: GraphEdge[]; total_memories?: number }

/** Pick an icon based on the entity label text */
function EntityIcon({ label }: { label: string }) {
  const lower = (label || '').toLowerCase()
  if (lower.includes('code') || lower.includes('python') || lower.includes('javascript') || lower.includes('java'))
    return <Code size={24} />
  if (lower.includes('gpu') || lower.includes('cuda') || lower.includes('cpu') || lower.includes('ml'))
    return <Cpu size={24} />
  if (lower.includes('tag') || lower.includes('topic') || lower.includes('category'))
    return <Tag size={24} />
  return <Network size={24} />
}

export default function Connections() {
  const [connections, setConnections] = useState<ConnectionsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      const data = await api.getConnections()
      setConnections(data)
      setLoading(false)
    }
    fetchData()
  }, [])

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title letterpress">Memory Connections</h1>
          <p className="page-subtitle">Discover relationships between your apps, topics, and sessions.</p>
        </div>
        {connections && (
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <span className="badge badge-outline">{connections.nodes?.length || 0} nodes</span>
            <span className="badge badge-outline">{connections.edges?.length || 0} edges</span>
          </div>
        )}
      </div>

      <div className="card" style={{ minHeight: '520px', display: 'flex', flexDirection: 'column' }}>
        {loading ? (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
            <div style={{ width: '52px', height: '52px', border: '4px solid #DBEAFE', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }}></div>
            <p style={{ color: 'var(--secondary-text)' }}>Analyzing semantic relationships...</p>
          </div>
        ) : connections && connections.nodes?.length > 0 ? (
          <>
            {/* Summary bar */}
            <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--secondary-text)' }}>
                <span style={{ fontWeight: 700, color: 'var(--primary-text)' }}>
                  {connections.nodes.filter(n => n.type === 'memory').length}
                </span> memories
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--secondary-text)' }}>
                <span style={{ fontWeight: 700, color: 'var(--primary-text)' }}>
                  {connections.nodes.filter(n => n.type === 'entity').length}
                </span> entities
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--secondary-text)' }}>
                <span style={{ fontWeight: 700, color: 'var(--primary-text)' }}>
                  {connections.edges.length}
                </span> relationships
              </div>
            </div>

            <div className="connections-grid" style={{ padding: '20px' }}>
              {connections.nodes
                .filter(n => n.type === 'entity')
                .map(node => {
                  const connectedEdges = connections.edges.filter(
                    e => e.source === node.id || e.target === node.id
                  )
                  const memoryCount = connectedEdges.length
                  if (memoryCount === 0) return null

                  return (
                    <div key={node.id} className="connection-node">
                      <div className="connection-icon">
                        {/* Backend returns node.label, NOT node.name */}
                        <EntityIcon label={node.label} />
                      </div>
                      <div style={{ fontFamily: 'var(--font-serif)', fontWeight: 700, fontSize: '1.1rem', color: 'var(--primary-text)', marginBottom: '6px' }}>
                        {node.label}
                      </div>
                      <span className="badge badge-outline">
                        {memoryCount} {memoryCount === 1 ? 'memory' : 'memories'}
                      </span>

                      {/* Connected memory nodes */}
                      <div style={{ width: '100%', marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {connectedEdges.slice(0, 3).map((edge, i) => {
                          const targetId = edge.source === node.id ? edge.target : edge.source
                          const targetNode = connections.nodes.find(n => n.id === targetId)
                          if (!targetNode || targetNode.type === 'entity') return null
                          return (
                            <div
                              key={i}
                              style={{
                                background: '#F9FAFB',
                                borderRadius: '8px',
                                padding: '10px 12px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                fontSize: '0.8rem',
                                textAlign: 'left'
                              }}
                            >
                              <Monitor size={13} color="#9CA3AF" style={{ flexShrink: 0 }} />
                              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontWeight: 500 }}>
                                {/* targetNode also has label, not name */}
                                {targetNode.label || 'Memory'}
                              </span>
                            </div>
                          )
                        })}
                        {memoryCount > 3 && (
                          <div style={{ fontSize: '0.75rem', color: 'var(--accent)', fontWeight: 600 }}>
                            + {memoryCount - 3} more
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}
            </div>
          </>
        ) : (
          <div className="empty-state" style={{ flex: 1 }}>
            <div className="connection-icon" style={{ width: '60px', height: '60px' }}>
              <Link2 size={28} />
            </div>
            <div className="empty-title" style={{ marginTop: '16px' }}>No connections yet</div>
            <p>Capture more memories to discover the relationships between your topics and entities.</p>
          </div>
        )}
      </div>
    </div>
  )
}
