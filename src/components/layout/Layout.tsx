import type { ReactNode } from 'react';
import { 
  LayoutDashboard, 
  Layers, 
  Search, 
  Clock, 
  Network, 
  Lightbulb,
  MessageSquareCode
} from 'lucide-react';
import { NavLink } from 'react-router-dom';

type LayoutProps = {
  children: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-container">
      {/* Sidebar */}
      <aside className="sidebar">
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
          <NavItem icon={<MessageSquareCode size={18} />} label="Ask AI" to="/chat" highlight />
        </nav>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, backgroundColor: 'var(--color-background)', overflowY: 'auto' }}>
        {children}
      </main>
    </div>
  );
}

function NavItem({ icon, label, to, highlight }: { icon: ReactNode, label: string, to: string, highlight?: boolean }) {
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
        color: isActive ? 'var(--color-accent)' : highlight ? '#818cf8' : 'var(--color-secondary-text)',
        backgroundColor: isActive ? 'rgba(109, 92, 231, 0.1)' : highlight ? 'rgba(99,102,241,0.08)' : 'transparent',
        border: highlight && !isActive ? '1px solid rgba(99,102,241,0.25)' : '1px solid transparent',
        fontWeight: highlight ? 600 : 500,
        fontSize: '0.875rem',
        marginTop: highlight ? '0.5rem' : 0,
      })}
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
}
