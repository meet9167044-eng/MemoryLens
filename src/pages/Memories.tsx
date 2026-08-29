import React, { useEffect, useState } from 'react';
import { memoryService } from '../services/memoryService';
import { Memory } from '../types/memory';
import { Link } from 'react-router-dom';
import { AppWindow, Layers } from 'lucide-react';

export const Memories: React.FC = () => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const data = await memoryService.getMemories();
      setMemories(data);
      setLoading(false);
    };
    fetchData();
  }, []);

  return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', color: '#333' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '40px' }}>
        <Layers size={32} color="#111" />
        <h1 style={{ fontSize: '36px', fontWeight: 'bold', color: '#111', margin: 0 }}>All Memories</h1>
      </div>

      {loading ? (
        <p>Loading memories...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
          {memories.map(memory => (
            <Link to={`/memories/${memory.id}`} key={memory.id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <div style={{ border: '1px solid #eee', borderRadius: '12px', padding: '24px', backgroundColor: '#fff', boxShadow: '0 4px 6px rgba(0,0,0,0.05)', transition: 'all 0.2s ease', cursor: 'pointer', height: '100%', display: 'flex', flexDirection: 'column' }}
                   onMouseOver={(e) => {
                     e.currentTarget.style.transform = 'translateY(-4px)';
                     e.currentTarget.style.boxShadow = '0 10px 15px rgba(0,0,0,0.1)';
                   }}
                   onMouseOut={(e) => {
                     e.currentTarget.style.transform = 'translateY(0)';
                     e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.05)';
                   }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px', color: '#666', fontSize: '13px' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '500' }}><AppWindow size={16} /> {memory.source.app}</span>
                  <span>{new Date(memory.timestamp).toLocaleDateString()}</span>
                </div>
                <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px', color: '#111', lineHeight: '1.4' }}>{memory.content.title}</h3>
                <p style={{ color: '#555', lineHeight: '1.5', fontSize: '14px', flexGrow: 1 }}>{memory.content.summary}</p>
                
                <div style={{ display: 'flex', gap: '8px', marginTop: '20px', flexWrap: 'wrap' }}>
                  {memory.tags.map(tag => (
                    <span key={tag} style={{ padding: '4px 10px', backgroundColor: '#f0f4f8', color: '#0369a1', borderRadius: '16px', fontSize: '12px', fontWeight: '500' }}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
