import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

export function Connections() {
  const navigate = useNavigate();
  const [memories, setMemories] = useState<Memory[]>([]);

  useEffect(() => {
    async function loadData() {
      const allMemories = await memoryService.getMemories();
      setMemories(allMemories);
    }
    loadData();
  }, []);

  // Filter out memories that have no relationships to show in the map
  const connectedMemories = memories.filter(m => m.relatedMemories && m.relatedMemories.length > 0);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      <div>
        <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>Connections</Typography>
        <Typography variant="body" color="secondary">
          Explore how your digital memories interrelate.
        </Typography>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {connectedMemories.map(memory => (
          <div key={memory.id} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* Parent Node */}
            <Card 
              style={{ cursor: 'pointer', borderLeft: '4px solid var(--color-accent)' }}
              onClick={() => navigate(`/memories/${memory.id}`)}
            >
              <Typography variant="h3" style={{ marginBottom: '0.25rem' }}>{memory.content.title}</Typography>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                <Typography variant="caption" color="secondary">Central Memory</Typography>
                {memory.tags.map(tag => (
                  <span key={tag} style={{ fontSize: '0.7rem', color: 'var(--color-accent)' }}>#{tag}</span>
                ))}
              </div>
            </Card>

            {/* Children Nodes (Connections) */}
            <div style={{ 
              display: 'flex', 
              flexDirection: 'column', 
              gap: '0.75rem', 
              marginLeft: '2rem', 
              borderLeft: '2px dashed var(--color-border)', 
              paddingLeft: '1.5rem' 
            }}>
              {memory.relatedMemories.map((rel, idx) => {
                const targetMemory = memories.find(m => m.id === rel.memoryId);
                if (!targetMemory) return null;

                return (
                  <div key={idx} style={{ position: 'relative' }}>
                    {/* Horizontal connection line */}
                    <div style={{
                      position: 'absolute',
                      left: '-1.5rem',
                      top: '50%',
                      width: '1rem',
                      borderTop: '2px dashed var(--color-border)'
                    }} />

                    <Card 
                      style={{ cursor: 'pointer', padding: '1rem' }}
                      onClick={() => navigate(`/memories/${targetMemory.id}`)}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="h4">{targetMemory.content.title}</Typography>
                        <span style={{
                          fontSize: '0.7rem',
                          padding: '0.125rem 0.5rem',
                          backgroundColor: 'var(--color-surface)',
                          border: '1px solid var(--color-border)',
                          borderRadius: '12px',
                          color: 'var(--color-secondary-text)'
                        }}>
                          {rel.relationship.replace('_', ' ')}
                        </span>
                      </div>
                    </Card>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
        
        {connectedMemories.length === 0 && (
          <Typography variant="body" color="secondary">No connections found in the current dataset.</Typography>
        )}
      </div>
    </div>
  );
}
