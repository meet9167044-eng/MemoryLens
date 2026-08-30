import { Routes, Route } from "react-router-dom"
import { Layout } from "@/components/layout/Layout"
import Overview from "@/pages/Overview/Overview"
import Memories from "@/pages/Memories/Memories"
import MemoryDetail from "@/pages/MemoryDetail"
import Search from "@/pages/Search"
import Timeline from "@/pages/Timeline/Timeline"
import Connections from "@/pages/Connections/Connections"
import Insights from "@/pages/Insights/Insights"
import Chat from "@/pages/Chat/Chat"

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
  )
}
