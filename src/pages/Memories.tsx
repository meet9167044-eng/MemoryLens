import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { MemoryGridCard } from '@/components/memory/MemoryGridCard';

export function Memories() {
  const navigate = useNavigate();
  const [memories, setMemories] = useState<Memory[]>([]);

  useEffect(() => {
    async function loadData() {
      const allMemories = await memoryService.getMemories();
      setMemories(allMemories);
    }
    loadData();
  }, []);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Header section */}
      <div>
        <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>Memory Explorer</Typography>
        <Typography variant="body" color="secondary">
          Browsing {memories.length} captured digital memories.
        </Typography>
      </div>

      {/* Grid Content */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '1.5rem' 
      }}>
        {memories.map(memory => (
          <MemoryGridCard 
            key={memory.id} 
            memory={memory} 
            onClick={() => navigate(`/memories/${memory.id}`)}
          />
        ))}
      </div>

    </div>
  );
}
