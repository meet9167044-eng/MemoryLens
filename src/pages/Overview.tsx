import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { memoryService } from '@/services/memoryService';
import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';
import { MemoryListItem } from '@/components/memory/MemoryListItem';
import { Activity, Network, Hash, Clock } from 'lucide-react';

export function Overview() {
  const navigate = useNavigate();
  const [recentMemories, setRecentMemories] = useState<Memory[]>([]);
  const [topics, setTopics] = useState<{ topic: string; count: number }[]>([]);
  const [summary, setSummary] = useState<{ totalMemories: number; totalConnections: number; totalTopics: number; activityTimeHrs: number } | null>(null);

  useEffect(() => {
    async function loadData() {
      const allMemories = await memoryService.getMemories();
      setRecentMemories(allMemories.slice(0, 4));
      
      const recentTopics = await memoryService.getRecentTopics();
      setTopics(recentTopics.slice(0, 5));

      const activitySummary = await memoryService.getActivitySummary();
      setSummary(activitySummary);
    }
    loadData();
  }, []);

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Header section */}
      <div>
        <Typography variant="h1" style={{ marginBottom: '0.5rem' }}>Good morning, Virat.</Typography>
        <Typography variant="body" color="secondary">Here's what MemoryLens has understood from your recent activity.</Typography>
      </div>

      {/* Summary Stats */}
      {summary && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <StatCard icon={<Activity size={20} color="var(--color-accent)" />} value={summary.totalMemories} label="Memories Captured" />
          <StatCard icon={<Network size={20} color="#00b894" />} value={summary.totalConnections} label="Connections Found" />
          <StatCard icon={<Hash size={20} color="#fdcb6e" />} value={summary.totalTopics} label="Active Topics" />
          <StatCard icon={<Clock size={20} color="#0984e3" />} value={`${summary.activityTimeHrs}h`} label="Activity Logged" />
        </div>
      )}

      {/* Main Content Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        
        {/* Left Column: Recent Memories */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h3">Recent Memories</Typography>
            <span style={{ fontSize: '0.875rem', color: 'var(--color-accent)', cursor: 'pointer' }} onClick={() => navigate('/memories')}>
              View all
            </span>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {recentMemories.map(memory => (
              <MemoryListItem 
                key={memory.id} 
                memory={memory} 
                onClick={() => navigate(`/memories/${memory.id}`)}
              />
            ))}
          </div>
        </div>

        {/* Right Column: Topics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Top Topics */}
          <Card style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Typography variant="h3">Top Topics</Typography>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {topics.map((t, index) => {
                const maxCount = topics[0]?.count || 1;
                const percentage = (t.count / maxCount) * 100;
                return (
                  <div key={t.topic}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                      <Typography variant="body">{t.topic}</Typography>
                      <Typography variant="caption" color="secondary">{t.count}</Typography>
                    </div>
                    <div style={{ height: '6px', backgroundColor: 'var(--color-border)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ 
                        height: '100%', 
                        width: `${percentage}%`, 
                        backgroundColor: 'var(--color-accent)',
                        opacity: 1 - (index * 0.15) // Subtle gradient effect
                      }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
          
        </div>

      </div>
    </div>
  );
}

function StatCard({ icon, value, label }: { icon: React.ReactNode, value: string | number, label: string }) {
  return (
    <Card style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1.25rem' }}>
      <div style={{ 
        width: '40px', height: '40px', 
        borderRadius: '8px', 
        backgroundColor: 'var(--color-background)',
        display: 'flex', alignItems: 'center', justifyContent: 'center'
      }}>
        {icon}
      </div>
      <div>
        <Typography variant="h2" style={{ lineHeight: 1.1 }}>{value}</Typography>
        <Typography variant="caption" color="secondary">{label}</Typography>
      </div>
    </Card>
  );
}
