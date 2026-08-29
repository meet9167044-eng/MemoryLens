import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

export function MemoryDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [memory, setMemory] = useState<Memory | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      try {
        const data = await memoryService.getMemoryById(id);
        setMemory(data || null);
      } catch (error) {
        console.error("Failed to load memory", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  if (loading) {
    return (
      <div style={{ padding: '2rem' }}>
        <Typography variant="body" color="secondary">Loading memory...</Typography>
      </div>
    );
  }

  if (!memory) {
    return (
      <div style={{ padding: '2rem' }}>
        <Typography variant="h2">Memory not found</Typography>
        <button 
          onClick={() => navigate('/memories')}
          style={{
            marginTop: '1rem',
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--color-surface)',
            border: '1px solid var(--color-border)',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Back to Memories
        </button>
      </div>
    );
  }

  const date = new Date(memory.timestamp).toLocaleDateString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* Back navigation */}
      <div>
        <button 
          onClick={() => navigate('/memories')}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--color-secondary-text)',
            cursor: 'pointer',
            padding: 0,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.875rem'
          }}
        >
          ← Back to Explorer
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '2rem', alignItems: 'start' }}>
        
        {/* Left Column: Evidence (Screenshot) */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>{memory.content.title}</Typography>
            <Typography variant="body" color="secondary">
              Captured from <strong style={{ color: 'var(--color-primary-text)' }}>{memory.source.app}</strong> on {date}
            </Typography>
          </div>
          
          <Card style={{ padding: 0, overflow: 'hidden', backgroundColor: '#e5e5e5' }}>
            {memory.screenshot.imageUrl ? (
              <img 
                src={memory.screenshot.imageUrl} 
                alt="Memory screenshot" 
                style={{ width: '100%', height: 'auto', display: 'block' }} 
              />
            ) : (
              <div style={{ padding: '4rem', textAlign: 'center', color: 'var(--color-secondary-text)' }}>
                Screenshot not available
              </div>
            )}
          </Card>
        </div>

        {/* Right Column: Understanding, Classification, Relationships */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Understanding */}
          <Card style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="h3">Understanding</Typography>
            <div>
              <Typography variant="h4" style={{ marginBottom: '0.25rem' }}>Summary</Typography>
              <Typography variant="body" color="secondary">{memory.content.summary}</Typography>
            </div>
            
            {memory.content.ocrText && (
              <div>
                <Typography variant="h4" style={{ marginBottom: '0.5rem' }}>Extracted Text</Typography>
                <div style={{
                  backgroundColor: 'var(--color-background)',
                  padding: '1rem',
                  borderRadius: '6px',
                  border: '1px solid var(--color-border)',
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  color: 'var(--color-secondary-text)',
                  whiteSpace: 'pre-wrap',
                  maxHeight: '200px',
                  overflowY: 'auto'
                }}>
                  {memory.content.ocrText}
                </div>
              </div>
            )}
          </Card>

          {/* Classification */}
          <Card style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="h3">Classification</Typography>
            
            {memory.entities && memory.entities.length > 0 && (
              <div>
                <Typography variant="h4" style={{ marginBottom: '0.5rem' }}>Entities</Typography>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {memory.entities.map(entity => (
                    <span key={entity.id} style={{
                      fontSize: '0.75rem',
                      padding: '0.25rem 0.75rem',
                      backgroundColor: 'rgba(109, 92, 231, 0.1)',
                      color: 'var(--color-accent)',
                      borderRadius: '16px',
                      fontWeight: 500,
                      border: '1px solid rgba(109, 92, 231, 0.2)'
                    }}>
                      {entity.name} ({entity.type})
                    </span>
                  ))}
                </div>
              </div>
            )}

            {memory.tags && memory.tags.length > 0 && (
              <div>
                <Typography variant="h4" style={{ marginBottom: '0.5rem' }}>Tags</Typography>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {memory.tags.map(tag => (
                    <span key={tag} style={{
                      fontSize: '0.75rem',
                      padding: '0.25rem 0.75rem',
                      backgroundColor: 'var(--color-background)',
                      color: 'var(--color-secondary-text)',
                      borderRadius: '16px',
                      border: '1px solid var(--color-border)'
                    }}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </Card>

          {/* Relationships */}
          <Card style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="h3">Relationships</Typography>
            {memory.relatedMemories && memory.relatedMemories.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {memory.relatedMemories.map((related, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    backgroundColor: 'var(--color-background)',
                    borderRadius: '6px',
                    border: '1px solid var(--color-border)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <Typography variant="body" style={{ fontWeight: 500 }}>
                      Related Memory: {related.memoryId}
                    </Typography>
                    <span style={{
                      fontSize: '0.75rem',
                      color: 'var(--color-secondary-text)',
                      backgroundColor: 'var(--color-surface)',
                      padding: '0.125rem 0.5rem',
                      borderRadius: '4px',
                      border: '1px solid var(--color-border)'
                    }}>
                      {related.relationship.replace('_', ' ')} ({(related.similarityScore || 0) * 100}%)
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <Typography variant="body" color="secondary">No related memories found.</Typography>
            )}
          </Card>

        </div>
      </div>
    </div>
  );
}
