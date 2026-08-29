import { Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import { Overview } from '@/pages/Overview';
import { Memories } from '@/pages/Memories';

// Placeholder components for other routes
const Placeholder = ({ title }: { title: string }) => (
  <div style={{ padding: '2rem' }}>
    <h1 style={{ fontSize: '1.5rem', fontWeight: 600 }}>{title}</h1>
    <p style={{ color: 'var(--color-secondary-text)', marginTop: '1rem' }}>
      This screen will be built in a future phase.
    </p>
  </div>
);

export function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/memories" element={<Memories />} />
        <Route path="/memories/:id" element={<Placeholder title="Memory Detail" />} />
        <Route path="/search" element={<Placeholder title="Search" />} />
        <Route path="/timeline" element={<Placeholder title="Timeline" />} />
        <Route path="/connections" element={<Placeholder title="Connections" />} />
        <Route path="/insights" element={<Placeholder title="Insights" />} />
      </Routes>
    </Layout>
  );
}
