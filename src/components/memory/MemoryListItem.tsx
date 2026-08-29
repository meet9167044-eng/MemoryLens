import { Memory } from '@/types/memory';
import { Typography } from '@/components/ui/Typography';
import { Card } from '@/components/ui/Card';

type MemoryListItemProps = {
  memory: Memory;
  onClick?: () => void;
};

export function MemoryListItem({ memory, onClick }: MemoryListItemProps) {
  const date = new Date(memory.timestamp).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
    <Card 
      onClick={onClick}
      style={{ 
        cursor: onClick ? 'pointer' : 'default',
        padding: '1rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
        transition: 'border-color 0.2s',
      }}
      onMouseEnter={(e) => {
        if (onClick) e.currentTarget.style.borderColor = 'var(--color-accent)';
      }}
      onMouseLeave={(e) => {
        if (onClick) e.currentTarget.style.borderColor = 'var(--color-border)';
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Typography variant="h4">{memory.content.title}</Typography>
        <Typography variant="caption" color="secondary">{date}</Typography>
      </div>
      
      <Typography variant="body" color="secondary" style={{ 
        display: '-webkit-box',
        WebkitLineClamp: 2,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden'
      }}>
        {memory.content.summary}
      </Typography>
      
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
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
