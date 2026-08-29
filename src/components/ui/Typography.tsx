import type { ReactNode, CSSProperties } from 'react';

type TypographyProps = {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'body' | 'caption';
  color?: 'primary' | 'secondary' | 'accent';
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
};

export function Typography({
  variant = 'body',
  color = 'primary',
  children,
  className = '',
  style: propStyle,
}: TypographyProps) {
  const baseStyles: CSSProperties = {
    margin: 0,
    color: color === 'primary' 
      ? 'var(--color-primary-text)' 
      : color === 'secondary' 
        ? 'var(--color-secondary-text)' 
        : 'var(--color-accent)',
  };

  const variantStyles: Record<string, CSSProperties> = {
    h1: { fontSize: '1.75rem', fontWeight: 600, lineHeight: 1.2 },
    h2: { fontSize: '1.5rem', fontWeight: 600, lineHeight: 1.3 },
    h3: { fontSize: '1.25rem', fontWeight: 600, lineHeight: 1.4 },
    h4: { fontSize: '1rem', fontWeight: 600, lineHeight: 1.5 },
    body: { fontSize: '0.875rem', fontWeight: 400, lineHeight: 1.5 },
    caption: { fontSize: '0.75rem', fontWeight: 400, lineHeight: 1.5 },
  };

  const Tag = variant.startsWith('h') ? (variant as keyof JSX.IntrinsicElements) : 'p';
  const style = { ...baseStyles, ...variantStyles[variant], ...propStyle };

  return (
    <Tag style={style} className={className}>
      {children}
    </Tag>
  );
}
