import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { format } from "date-fns"
import { api, SearchResult } from "@/services/api"
import { Search as SearchIcon, Clock, Layers, Loader, SlidersHorizontal, X } from "lucide-react"

const SOURCE_TYPES = ["desktop", "browser", "terminal", "document", "other"]

export default function Search() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<SearchResult[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [showFilters, setShowFilters] = useState(false)
  const [sourceType, setSourceType] = useState("")
  const [dateFrom, setDateFrom] = useState("")
  const [dateTo, setDateTo] = useState("")
  const navigate = useNavigate()

  const handleSearch = async (e?: React.FormEvent) => {
    e?.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setHasSearched(true)

    const res = await api.searchMemories({
      q: query,
      limit: 20,
      source_type: sourceType || undefined,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
    })

    setResults(res?.results || [])
    setTotal(res?.total || 0)
    setLoading(false)
  }

  const clearFilters = () => { setSourceType(""); setDateFrom(""); setDateTo("") }
  const hasFilters = !!(sourceType || dateFrom || dateTo)

  return (
    <div>
      {/* Header */}
      <div style={{ textAlign: 'center', padding: '40px 0 36px' }}>
        <h1 className="page-title letterpress" style={{ marginBottom: '12px' }}>Hybrid Search</h1>
        <p className="page-subtitle" style={{ maxWidth: '500px', margin: '0 auto 36px' }}>
          Search your digital memory by keyword, semantic meaning, or entity name.
        </p>

        <form onSubmit={handleSearch} style={{ maxWidth: '680px', margin: '0 auto' }}>
          <div className="search-bar-wrap">
            <SearchIcon className="search-icon" size={22} />
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="e.g. 'GPU debugging in python' or 'CUDA environment setup'"
              className="search-input"
            />
            <button
              type="button"
              title="Filters"
              onClick={() => setShowFilters(!showFilters)}
              style={{ padding: '8px 12px', marginRight: '4px', background: hasFilters ? '#EFF6FF' : 'transparent', border: hasFilters ? '1px solid #DBEAFE' : 'none', borderRadius: '8px', cursor: 'pointer', color: hasFilters ? 'var(--accent)' : '#9CA3AF', display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.8rem', fontWeight: 500 }}
            >
              <SlidersHorizontal size={16} />
              {hasFilters ? 'Filtered' : 'Filter'}
            </button>
            <button type="submit" disabled={loading || !query.trim()} className="search-submit">
              {loading ? <Loader size={17} style={{ animation: 'spin 1s linear infinite' }} /> : 'Search'}
            </button>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div style={{ background: '#fff', border: '1px solid var(--border)', borderRadius: '12px', padding: '18px 20px', marginTop: '10px', textAlign: 'left', boxShadow: '0 4px 16px rgba(0,0,0,0.06)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--primary-text)' }}>Filters</span>
                {hasFilters && (
                  <button onClick={clearFilters} style={{ fontSize: '0.75rem', color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <X size={12} /> Clear all
                  </button>
                )}
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--secondary-text)', display: 'block', marginBottom: '6px' }}>SOURCE TYPE</label>
                  <select
                    value={sourceType}
                    onChange={e => setSourceType(e.target.value)}
                    style={{ width: '100%', padding: '8px 10px', borderRadius: '8px', border: '1px solid var(--border)', fontSize: '0.85rem', background: '#fff', cursor: 'pointer' }}
                  >
                    <option value="">All types</option>
                    {SOURCE_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--secondary-text)', display: 'block', marginBottom: '6px' }}>FROM DATE</label>
                  <input
                    type="date"
                    value={dateFrom}
                    onChange={e => setDateFrom(e.target.value)}
                    style={{ width: '100%', padding: '8px 10px', borderRadius: '8px', border: '1px solid var(--border)', fontSize: '0.85rem', background: '#fff' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--secondary-text)', display: 'block', marginBottom: '6px' }}>TO DATE</label>
                  <input
                    type="date"
                    value={dateTo}
                    onChange={e => setDateTo(e.target.value)}
                    style={{ width: '100%', padding: '8px 10px', borderRadius: '8px', border: '1px solid var(--border)', fontSize: '0.85rem', background: '#fff' }}
                  />
                </div>
              </div>
            </div>
          )}
        </form>
      </div>

      {/* Results */}
      {hasSearched && (
        <div style={{ borderTop: '1px solid var(--border)', paddingTop: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 600, color: 'var(--primary-text)' }}>
              {loading ? "Searching…" : `${total} result${total !== 1 ? 's' : ''} for "${query}"`}
            </h2>
          </div>

          {loading ? (
            <div className="memory-card-list">
              {[1, 2, 3].map(i => <div key={i} className="skeleton" style={{ height: '110px' }}></div>)}
            </div>
          ) : results.length > 0 ? (
            <div className="memory-card-list">
              {results.map(result => (
                <div key={result.id} className="memory-card-row" onClick={() => navigate(`/memories/${result.id}`)}>
                  {/* Thumbnail — SearchResult has image_url (flat path) */}
                  <div className="memory-card-thumb" style={{ minHeight: '100px' }}>
                    {result.image_url ? (
                      <img
                        src={result.image_url}
                        alt=""
                        onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
                      />
                    ) : (
                      <Layers size={28} color="#D1D5DB" />
                    )}
                  </div>

                  <div className="memory-card-body">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '4px' }}>
                      {/* SearchResult has flat title field */}
                      <div className="memory-card-title" style={{ flex: 1 }}>{result.title || 'Untitled'}</div>
                      <div style={{ display: 'flex', gap: '6px', marginLeft: '12px', flexShrink: 0 }}>
                        <span className="badge badge-accent">{result.source?.app || result.source?.type}</span>
                        {result.relevance_score > 0 && (
                          <span className="badge badge-outline" style={{ fontSize: '0.65rem' }}>
                            {Math.round(result.relevance_score * 100)}%
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="memory-card-meta" style={{ marginBottom: '4px' }}>
                      <Clock size={12} />
                      <span>{format(new Date(result.timestamp || new Date()), "MMM d, yyyy h:mm a")}</span>
                    </div>
                    {/* SearchResult has flat summary field */}
                    <div className="memory-card-summary">{result.summary}</div>
                    {/* OCR snippet when available */}
                    {result.ocr_snippet && (
                      <div style={{ marginTop: '6px', fontSize: '0.75rem', color: 'var(--secondary-text)', fontFamily: 'monospace', background: '#F9FAFB', padding: '4px 8px', borderRadius: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {result.ocr_snippet}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-icon"><SearchIcon size={28} /></div>
              <div className="empty-title">No results found</div>
              <p>Try different keywords, or check the backend is running.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
