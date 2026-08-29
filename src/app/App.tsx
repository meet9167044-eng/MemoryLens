import { Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import { Overview } from '@/pages/Overview';
import { Memories } from '@/pages/Memories';
import { MemoryDetail } from '@/pages/MemoryDetail';
import { Search } from '@/pages/Search';
import { Timeline } from '@/pages/Timeline';
import { Connections } from '@/pages/Connections';
import { Insights } from '@/pages/Insights';
import { Chat } from '@/pages/Chat';

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
        <Route path="/memories/:id" element={<MemoryDetail />} />
        <Route path="/search" element={<Search />} />
        <Route path="/timeline" element={<Timeline />} />
        <Route path="/connections" element={<Connections />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Layout>
  );
}
