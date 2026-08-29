import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

type MemoryGridCardProps = {
  memory: Memory;
  onClick?: () => void;
};

export function MemoryGridCard({ memory, onClick }: MemoryGridCardProps) {
  const date = new Date(memory.timestamp).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
    <Card 
      onClick={onClick}
      style={{ 
        cursor: onClick ? 'pointer' : 'default',
        padding: '1.25rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        transition: 'border-color 0.2s, box-shadow 0.2s',
        height: '100%',
        justifyContent: 'space-between'
      }}
      onMouseEnter={(e) => {
        if (onClick) {
          e.currentTarget.style.borderColor = 'var(--color-accent)';
          e.currentTarget.style.boxShadow = '0 2px 8px rgba(109, 92, 231, 0.1)';
        }
      }}
      onMouseLeave={(e) => {
        if (onClick) {
          e.currentTarget.style.borderColor = 'var(--color-border)';
          e.currentTarget.style.boxShadow = 'none';
        }
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Typography variant="h4" style={{ WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', display: '-webkit-box', overflow: 'hidden' }}>
            {memory.content.title}
          </Typography>
        </div>
        
        <Typography variant="caption" color="secondary">{date}</Typography>
        
        <Typography variant="body" color="secondary" style={{ 
          display: '-webkit-box',
          WebkitLineClamp: 3,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden',
          marginTop: '0.25rem'
        }}>
          {memory.content.summary}
        </Typography>
      </div>
      
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
        <span style={{
          fontSize: '0.75rem',
          padding: '0.125rem 0.5rem',
          backgroundColor: 'rgba(109, 92, 231, 0.1)',
          color: 'var(--color-accent)',
          borderRadius: '12px',
          fontWeight: 500
        }}>
          {memory.source.app}
        </span>
        {memory.tags.slice(0, 3).map(tag => (
          <span key={tag} style={{
            fontSize: '0.75rem',
            padding: '0.125rem 0.5rem',
            backgroundColor: 'var(--color-background)',
            color: 'var(--color-secondary-text)',
            borderRadius: '12px',
            border: '1px solid var(--color-border)'
          }}>
            #{tag}
          </span>
        ))}
      </div>
    </Card>
  );
}
