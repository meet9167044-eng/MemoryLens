import React, { useEffect, useState } from 'react';
import { memoryService } from '../services/memoryService';
import { Memory } from '../types/memory';
import { Link } from 'react-router-dom';
import { Calendar, Clock, AppWindow } from 'lucide-react';

export const Timeline: React.FC = () => {
  const [groupedMemories, setGroupedMemories] = useState<Record<string, Memory[]>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const data = await memoryService.getMemories();
      
      // Group by date string
      const grouped: Record<string, Memory[]> = {};
      data.forEach(memory => {
        const dateObj = new Date(memory.timestamp);
        // Format: "August 29, 2026"
        const dateString = dateObj.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
        
        if (!grouped[dateString]) {
          grouped[dateString] = [];
        }
        grouped[dateString].push(memory);
      });

      setGroupedMemories(grouped);
      setLoading(false);
    };
    
    fetchData();
  }, []);

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', color: '#333' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '40px' }}>
        <Calendar size={32} color="#111" />
        <h1 style={{ fontSize: '36px', fontWeight: 'bold', color: '#111', margin: 0 }}>Timeline</h1>
      </div>

      {loading ? (
        <p>Loading timeline...</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', position: 'relative' }}>
          {/* Vertical line connecting timeline items */}
          <div style={{ position: 'absolute', left: '20px', top: '10px', bottom: '0', width: '2px', backgroundColor: '#e5e7eb', zIndex: 0 }}></div>

          {Object.entries(groupedMemories).map(([dateStr, memories]) => (
            <div key={dateStr} style={{ position: 'relative', zIndex: 1 }}>
              {/* Date Header */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
                <div style={{ width: '42px', height: '42px', borderRadius: '50%', backgroundColor: '#f3f4f6', border: '2px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                  <Calendar size={20} color="#4b5563" />
                </div>
                <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#111', margin: 0, backgroundColor: '#fff', padding: '4px 12px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
                  {dateStr}
                </h2>
              </div>

              {/* Memories for this date */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginLeft: '58px' }}>
                {memories.map(memory => (
                  <Link to={`/memories/${memory.id}`} key={memory.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div style={{ 
                      border: '1px solid #eee', 
                      borderRadius: '12px', 
                      padding: '20px', 
                      backgroundColor: '#fff', 
                      boxShadow: '0 2px 4px rgba(0,0,0,0.02)',
                      transition: 'transform 0.2s ease, box-shadow 0.2s ease'
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.boxShadow = '0 6px 12px rgba(0,0,0,0.05)';
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#111', margin: 0 }}>{memory.content.title}</h3>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#6b7280', fontSize: '13px', backgroundColor: '#f9fafb', padding: '4px 8px', borderRadius: '6px' }}>
                          <Clock size={14} />
                          {new Date(memory.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                      
                      <p style={{ color: '#4b5563', margin: '0 0 16px 0', fontSize: '14px', lineHeight: '1.5' }}>{memory.content.summary}</p>
                      
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#6b7280', fontSize: '13px', fontWeight: '500' }}>
                          <AppWindow size={14} /> {memory.source.app}
                        </div>
                        <div style={{ display: 'flex', gap: '6px' }}>
                          {memory.tags.slice(0, 3).map(tag => (
                            <span key={tag} style={{ padding: '2px 8px', backgroundColor: '#f3f4f6', color: '#374151', borderRadius: '12px', fontSize: '11px', fontWeight: '500' }}>
                              #{tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
