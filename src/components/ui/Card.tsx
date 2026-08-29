import type { HTMLAttributes, CSSProperties } from 'react';

type CardProps = HTMLAttributes<HTMLDivElement>;

export function Card({ children, style, ...props }: CardProps) {
  const cardStyle: CSSProperties = {
    backgroundColor: 'var(--color-surface)',
    borderRadius: '8px',
    border: '1px solid var(--color-border)',
    padding: '1.5rem',
    ...style,
  };

  return (
    <div style={cardStyle} {...props}>
      {children}
    </div>
  );
}
