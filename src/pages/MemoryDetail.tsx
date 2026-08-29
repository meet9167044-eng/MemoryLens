import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { memoryService } from '../services/memoryService';
import { Memory } from '../types/memory';
import { ArrowLeft, Image as ImageIcon, Brain, Tag, Link2, AppWindow } from 'lucide-react';

export const MemoryDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [memory, setMemory] = useState<Memory | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMemory = async () => {
      if (id) {
        setLoading(true);
        const data = await memoryService.getMemoryById(id);
        setMemory(data || null);
        setLoading(false);
      }
    };
    fetchMemory();
  }, [id]);

  if (loading) {
    return <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>Loading memory details...</div>;
  }

  if (!memory) {
    return (
      <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
        <h2>Memory not found</h2>
        <button onClick={() => navigate(-1)} style={{ padding: '8px 16px', cursor: 'pointer' }}>Go Back</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '40px', maxWidth: '900px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', color: '#333' }}>
      <button 
        onClick={() => navigate(-1)} 
        style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'none', border: 'none', color: '#666', cursor: 'pointer', padding: '0 0 24px 0', fontSize: '16px', fontWeight: '500' }}>
        <ArrowLeft size={20} /> Back
      </button>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' }}>
        <h1 style={{ fontSize: '36px', fontWeight: 'bold', color: '#111', margin: 0, lineHeight: '1.2' }}>{memory.content.title}</h1>
        <div style={{ textAlign: 'right', color: '#666' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '6px', marginBottom: '4px', fontWeight: '500' }}>
            <AppWindow size={16} /> {memory.source.app}
          </div>
          <div style={{ fontSize: '14px' }}>{new Date(memory.timestamp).toLocaleString()}</div>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
        
        {/* 1. Evidence */}
        <section>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#111' }}>
            <ImageIcon size={20} /> Evidence
          </h2>
          <div style={{ borderRadius: '12px', overflow: 'hidden', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
            <img src={memory.screenshot.imageUrl} alt="Memory evidence" style={{ width: '100%', display: 'block' }} />
          </div>
        </section>

        {/* 2. Understanding */}
        <section>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#111' }}>
            <Brain size={20} /> Understanding
          </h2>
          <div style={{ backgroundColor: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '24px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '8px', color: '#374151' }}>Summary</h3>
            <p style={{ color: '#4b5563', lineHeight: '1.6', marginBottom: '24px', fontSize: '15px' }}>{memory.content.summary}</p>
            
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '8px', color: '#374151' }}>OCR Text Extraction</h3>
            <div style={{ backgroundColor: '#1f2937', color: '#f3f4f6', padding: '16px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '13px', lineHeight: '1.5', whiteSpace: 'pre-wrap', overflowX: 'auto' }}>
              {memory.content.ocrText}
            </div>
          </div>
        </section>

        {/* 3. Classification */}
        <section>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#111' }}>
            <Tag size={20} /> Classification
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
            <div style={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '20px' }}>
              <h3 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Entities</h3>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {memory.entities.map(entity => (
                  <span key={entity.id} style={{ padding: '6px 12px', backgroundColor: '#fdf4ff', color: '#86198f', borderRadius: '6px', fontSize: '14px', fontWeight: '500', border: '1px solid #f0abfc' }}>
                    {entity.name} <span style={{ fontSize: '11px', opacity: 0.7, marginLeft: '4px' }}>({entity.type})</span>
                  </span>
                ))}
                {memory.entities.length === 0 && <span style={{ color: '#9ca3af', fontSize: '14px' }}>No entities found.</span>}
              </div>
            </div>
            
            <div style={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '20px' }}>
              <h3 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Tags</h3>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {memory.tags.map(tag => (
                  <span key={tag} style={{ padding: '6px 12px', backgroundColor: '#f0f9ff', color: '#0369a1', borderRadius: '20px', fontSize: '14px', fontWeight: '500', border: '1px solid #bae6fd' }}>
                    #{tag}
                  </span>
                ))}
                {memory.tags.length === 0 && <span style={{ color: '#9ca3af', fontSize: '14px' }}>No tags found.</span>}
              </div>
            </div>
          </div>
        </section>

        {/* 4. Relationships */}
        <section>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#111' }}>
            <Link2 size={20} /> Relationships
          </h2>
          <div style={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '24px' }}>
            {memory.relatedMemories.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {memory.relatedMemories.map(rel => (
                  <Link to={`/memories/${rel.memoryId}`} key={rel.memoryId} style={{ textDecoration: 'none' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 16px', backgroundColor: '#f9fafb', borderRadius: '8px', border: '1px solid #f3f4f6', transition: 'background-color 0.2s' }}
                         onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f3f4f6'}
                         onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#f9fafb'}>
                      <span style={{ color: '#374151', fontWeight: '500' }}>Memory {rel.memoryId}</span>
                      <span style={{ fontSize: '12px', padding: '4px 8px', backgroundColor: '#e5e7eb', color: '#4b5563', borderRadius: '4px', textTransform: 'capitalize' }}>
                        {rel.relationship.replace('_', ' ')}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p style={{ color: '#6b7280', margin: 0, fontSize: '15px' }}>No related memories found.</p>
            )}
          </div>
        </section>

      </div>
    </div>
  );
};
