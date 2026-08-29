import React, { useEffect, useState } from 'react';
import { memoryService } from '../services/memoryService';
import { Memory } from '../types/memory';
import { Link } from 'react-router-dom';
import { Clock, Tag, AppWindow } from 'lucide-react';

export const Overview: React.FC = () => {
  const [recentMemories, setRecentMemories] = useState<Memory[]>([]);
  const [topTopics, setTopTopics] = useState<{name: string, count: number}[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const memories = await memoryService.getMemories();
      setRecentMemories(memories.slice(0, 3));
      const topics = await memoryService.getRecentTopics();
      setTopTopics(topics);
      setLoading(false);
    };
    fetchData();
  }, []);

  return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', color: '#333' }}>
      <h1 style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '40px', color: '#111' }}>
        Good morning, Virat.
      </h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '40px' }}>
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Clock size={24} /> Recent Memories
          </h2>
          
          {loading ? (
            <p>Loading memories...</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {recentMemories.map(memory => (
                <Link to={`/memories/${memory.id}`} key={memory.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div style={{ border: '1px solid #eee', borderRadius: '12px', padding: '24px', backgroundColor: '#fff', boxShadow: '0 4px 6px rgba(0,0,0,0.05)', transition: 'transform 0.2s', cursor: 'pointer' }}
                       onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
                       onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px', color: '#666', fontSize: '14px' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><AppWindow size={16} /> {memory.source.app}</span>
                      <span>{new Date(memory.timestamp).toLocaleString()}</span>
                    </div>
                    <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '10px', color: '#111' }}>{memory.content.title}</h3>
                    <p style={{ color: '#555', lineHeight: '1.5' }}>{memory.content.summary}</p>
                    <div style={{ display: 'flex', gap: '8px', marginTop: '16px', flexWrap: 'wrap' }}>
                      {memory.tags.map(tag => (
                        <span key={tag} style={{ padding: '4px 12px', backgroundColor: '#f0f4f8', color: '#0369a1', borderRadius: '20px', fontSize: '12px', fontWeight: '500' }}>
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

        <div>
          <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Tag size={24} /> Top Topics
          </h2>
          <div style={{ border: '1px solid #eee', borderRadius: '12px', padding: '24px', backgroundColor: '#fff', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
            {loading ? (
              <p>Loading topics...</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {topTopics.map((topic, idx) => (
                  <div key={topic.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span style={{ color: '#999', fontWeight: 'bold', fontSize: '14px' }}>0{idx + 1}</span>
                      <span style={{ fontWeight: '500', color: '#333', textTransform: 'capitalize' }}>{topic.name}</span>
                    </div>
                    <span style={{ backgroundColor: '#f3f4f6', padding: '2px 8px', borderRadius: '12px', fontSize: '12px', color: '#666' }}>
                      {topic.count}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
