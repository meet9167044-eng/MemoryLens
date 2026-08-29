import { useEffect, useState } from 'react';
import { memoryService } from '@/services/memoryService';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

export function Insights() {
  const [insights, setInsights] = useState<any[]>([]);
  const [topics, setTopics] = useState<any[]>([]);

  useEffect(() => {
    async function loadData() {
      const [fetchedInsights, fetchedTopics] = await Promise.all([
        memoryService.getInsights(),
        memoryService.getRecentTopics()
      ]);
      setInsights(fetchedInsights);
      setTopics(fetchedTopics);
    }
    loadData();
  }, []);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '3rem', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
      
      <div>
        <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>Insights</Typography>
        <Typography variant="body" color="secondary">
          AI-generated patterns based on your digital history.
        </Typography>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        
        {/* Identified Patterns */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <Typography variant="h2">Identified Patterns</Typography>
          {insights.map(insight => (
            <Card key={insight.id} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Typography variant="h3">{insight.title}</Typography>
                <span style={{
                  fontSize: '0.7rem',
                  padding: '0.2rem 0.5rem',
                  backgroundColor: 'rgba(109, 92, 231, 0.1)',
                  color: 'var(--color-accent)',
                  borderRadius: '12px',
                  fontWeight: 600,
                  textTransform: 'uppercase'
                }}>
                  {insight.type.replace('_', ' ')}
                </span>
              </div>
              <Typography variant="body" color="secondary">{insight.description}</Typography>
              <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--color-primary-text)', fontWeight: 500 }}>
                Supported by {insight.memoryCount} memories
              </div>
            </Card>
          ))}
        </div>

        {/* Top Entities/Topics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <Typography variant="h2">Frequent Topics</Typography>
          <Card style={{ padding: 0, overflow: 'hidden' }}>
            {topics.map((topic, index) => (
              <div key={topic.topic} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                padding: '1.25rem',
                borderBottom: index < topics.length - 1 ? '1px solid var(--color-border)' : 'none'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ color: 'var(--color-secondary-text)', fontWeight: 600, width: '1.5rem' }}>#{index + 1}</span>
                  <Typography variant="body" style={{ fontWeight: 500 }}>{topic.topic}</Typography>
                </div>
                <Typography variant="caption" color="secondary">{topic.count} mentions</Typography>
              </div>
            ))}
          </Card>
        </div>

      </div>

    </div>
  );
}
