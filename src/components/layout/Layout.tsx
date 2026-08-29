import type { ReactNode } from 'react';
import { 
  LayoutDashboard, 
  Layers, 
  Search, 
  Clock, 
  Network, 
  Lightbulb 
} from 'lucide-react';
import { NavLink } from 'react-router-dom';

type LayoutProps = {
  children: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', width: '100%' }}>
      {/* Sidebar */}
      <aside style={{
        width: '240px',
        borderRight: '1px solid var(--color-border)',
        backgroundColor: 'var(--color-surface)',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{ padding: '1.5rem', fontWeight: 600, fontSize: '1.125rem' }}>
          MemoryLens
        </div>
        
        <nav style={{ padding: '0 1rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <NavItem icon={<LayoutDashboard size={18} />} label="Overview" to="/" />
          <NavItem icon={<Layers size={18} />} label="Memories" to="/memories" />
          <NavItem icon={<Search size={18} />} label="Search" to="/search" />
          <NavItem icon={<Clock size={18} />} label="Timeline" to="/timeline" />
          <NavItem icon={<Network size={18} />} label="Connections" to="/connections" />
          <NavItem icon={<Lightbulb size={18} />} label="Insights" to="/insights" />
        </nav>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, backgroundColor: 'var(--color-background)', overflowY: 'auto' }}>
        {children}
      </main>
    </div>
  );
}

function NavItem({ icon, label, to }: { icon: ReactNode, label: string, to: string }) {
  return (
    <NavLink 
      to={to}
      style={({ isActive }) => ({
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        padding: '0.5rem 0.75rem',
        borderRadius: '6px',
        cursor: 'pointer',
        color: isActive ? 'var(--color-accent)' : 'var(--color-secondary-text)',
        backgroundColor: isActive ? 'rgba(109, 92, 231, 0.1)' : 'transparent',
        fontWeight: 500,
        fontSize: '0.875rem',
      })}
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
}
