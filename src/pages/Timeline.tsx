import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

// Grouping helper
function groupMemoriesByDate(memories: Memory[]) {
  const grouped: Record<string, Memory[]> = {};
  memories.forEach(memory => {
    const dateStr = new Date(memory.timestamp).toLocaleDateString('en-US', {
      month: 'long', day: 'numeric', year: 'numeric'
    });
    if (!grouped[dateStr]) {
      grouped[dateStr] = [];
    }
    grouped[dateStr].push(memory);
  });
  return grouped;
}

export function Timeline() {
  const navigate = useNavigate();
  const [groupedMemories, setGroupedMemories] = useState<Record<string, Memory[]>>({});

  useEffect(() => {
    async function loadData() {
      const allMemories = await memoryService.getMemories();
      setGroupedMemories(groupMemoriesByDate(allMemories));
    }
    loadData();
  }, []);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
      
      <div>
        <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>Timeline</Typography>
        <Typography variant="body" color="secondary">
          Your digital history in chronological order.
        </Typography>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {Object.entries(groupedMemories).map(([date, memories]) => (
          <div key={date} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="h3" style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '0.5rem' }}>
              {date}
            </Typography>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', borderLeft: '2px solid var(--color-border)', paddingLeft: '1.5rem', marginLeft: '0.5rem' }}>
              {memories.map(memory => {
                const timeStr = new Date(memory.timestamp).toLocaleTimeString('en-US', {
                  hour: '2-digit', minute: '2-digit'
                });
                
                return (
                  <Card 
                    key={memory.id} 
                    onClick={() => navigate(`/memories/${memory.id}`)}
                    style={{ 
                      cursor: 'pointer',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.5rem',
                      transition: 'border-color 0.2s',
                      position: 'relative'
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--color-accent)'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--color-border)'; }}
                  >
                    {/* Timeline dot */}
                    <div style={{
                      position: 'absolute',
                      left: '-1.85rem',
                      top: '1.5rem',
                      width: '0.75rem',
                      height: '0.75rem',
                      backgroundColor: 'var(--color-surface)',
                      border: '2px solid var(--color-accent)',
                      borderRadius: '50%'
                    }} />

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h4">{memory.content.title}</Typography>
                      <Typography variant="caption" color="secondary">{timeStr}</Typography>
                    </div>
                    
                    <Typography variant="body" color="secondary" style={{ WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', display: '-webkit-box', overflow: 'hidden' }}>
                      {memory.content.summary}
                    </Typography>
                    
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', padding: '0.125rem 0.5rem', backgroundColor: 'rgba(109, 92, 231, 0.1)', color: 'var(--color-accent)', borderRadius: '12px' }}>
                        {memory.source.app}
                      </span>
                    </div>
                  </Card>
                );
              })}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
