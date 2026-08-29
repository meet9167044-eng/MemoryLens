import React, { useState, useEffect, useCallback } from 'react';
import { memoryService } from '../services/memoryService';
import { Memory } from '../types/memory';
import { Link } from 'react-router-dom';
import { Search as SearchIcon, AppWindow } from 'lucide-react';

export const Search: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Debounce the search call
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (query.trim() === '') {
        setResults([]);
        setHasSearched(false);
        setLoading(false);
        return;
      }
      
      setLoading(true);
      setHasSearched(true);
      const searchResults = await memoryService.searchMemories(query);
      setResults(searchResults);
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div style={{ padding: '40px', maxWidth: '1000px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', color: '#333' }}>
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ fontSize: '36px', fontWeight: 'bold', color: '#111', marginBottom: '16px' }}>Search Memories</h1>
        
        <div style={{ position: 'relative', maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af', display: 'flex' }}>
            <SearchIcon size={20} />
          </div>
          <input 
            type="text" 
            placeholder="Search by title, OCR text, tags, or entities..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '16px 16px 16px 48px', 
              fontSize: '16px', 
              borderRadius: '24px', 
              border: '1px solid #d1d5db',
              boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
              outline: 'none',
              boxSizing: 'border-box'
            }}
          />
        </div>
      </div>

      <div style={{ marginTop: '40px' }}>
        {loading && <div style={{ textAlign: 'center', color: '#6b7280' }}>Searching...</div>}
        
        {!loading && hasSearched && results.length === 0 && (
          <div style={{ textAlign: 'center', color: '#6b7280', padding: '40px', backgroundColor: '#f9fafb', borderRadius: '12px' }}>
            <p style={{ fontSize: '18px', fontWeight: '500' }}>No memories found matching "{query}"</p>
            <p style={{ marginTop: '8px' }}>Try using different keywords or tags.</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div>
            <h2 style={{ fontSize: '18px', color: '#6b7280', marginBottom: '24px', fontWeight: '500' }}>
              Found {results.length} result{results.length !== 1 ? 's' : ''}
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {results.map(memory => (
                <Link to={`/memories/${memory.id}`} key={memory.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div style={{ 
                    border: '1px solid #eee', 
                    borderRadius: '12px', 
                    padding: '20px', 
                    backgroundColor: '#fff', 
                    boxShadow: '0 2px 4px rgba(0,0,0,0.02)', 
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = 'translateX(4px)';
                    e.currentTarget.style.borderColor = '#d1d5db';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = 'translateX(0)';
                    e.currentTarget.style.borderColor = '#eee';
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#111', margin: 0 }}>{memory.content.title}</h3>
                      <span style={{ fontSize: '13px', color: '#6b7280' }}>{new Date(memory.timestamp).toLocaleDateString()}</span>
                    </div>
                    
                    <p style={{ color: '#4b5563', margin: 0, fontSize: '14px', lineHeight: '1.5' }}>{memory.content.summary}</p>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#6b7280', fontSize: '13px', fontWeight: '500' }}>
                        <AppWindow size={14} /> {memory.source.app}
                      </div>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        {memory.tags.slice(0, 3).map(tag => (
                          <span key={tag} style={{ padding: '2px 8px', backgroundColor: '#f3f4f6', color: '#374151', borderRadius: '12px', fontSize: '11px', fontWeight: '500' }}>
                            #{tag}
                          </span>
                        ))}
                        {memory.tags.length > 3 && <span style={{ fontSize: '11px', color: '#9ca3af' }}>+{memory.tags.length - 3} more</span>}
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
