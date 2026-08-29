import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { MemoryGridCard } from '@/components/memory/MemoryGridCard';

export function Search() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const performSearch = async () => {
      if (!query.trim()) {
        setResults([]);
        return;
      }
      setLoading(true);
      try {
        const matchingMemories = await memoryService.searchMemories(query);
        setResults(matchingMemories);
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(performSearch, 300);
    return () => clearTimeout(debounceTimer);
  }, [query]);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
      
      {/* Header & Search Bar */}
      <div>
        <Typography variant="h1" style={{ marginBottom: '1rem' }}>Search</Typography>
        <input 
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search memories, OCR text, tags, or entities..."
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1rem',
            borderRadius: '8px',
            border: '1px solid var(--color-border)',
            backgroundColor: 'var(--color-surface)',
            color: 'var(--color-primary-text)',
            outline: 'none',
          }}
        />
      </div>

      {/* Results */}
      <div>
        {loading ? (
          <Typography variant="body" color="secondary">Searching...</Typography>
        ) : query.trim() === '' ? (
          <Typography variant="body" color="secondary">Type something to begin searching.</Typography>
        ) : results.length === 0 ? (
          <Typography variant="body" color="secondary">No memories found for "{query}".</Typography>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="body" color="secondary">Found {results.length} result(s)</Typography>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
              gap: '1.5rem' 
            }}>
              {results.map(memory => (
                <MemoryGridCard 
                  key={memory.id} 
                  memory={memory} 
                  onClick={() => navigate(`/memories/${memory.id}`)}
                />
              ))}
            </div>
          </div>
        )}
      </div>

    </div>
  );
}
