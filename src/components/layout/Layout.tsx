import React from "react"
import { Link, useLocation } from "react-router-dom"
import { 
  LayoutDashboard, 
  Layers, 
  Search, 
  Clock, 
  Network, 
  BarChart3,
  MessageSquare,
  Eye
} from "lucide-react"

const navigation = [
  { name: "Overview", href: "/", icon: LayoutDashboard },
  { name: "Memories", href: "/memories", icon: Layers },
  { name: "Search", href: "/search", icon: Search },
  { name: "Timeline", href: "/timeline", icon: Clock },
  { name: "Connections", href: "/connections", icon: Network },
  { name: "Insights", href: "/insights", icon: BarChart3 },
  { name: "AI Chat", href: "/chat", icon: MessageSquare },
]

export function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">
            <Eye size={20} color="white" />
          </div>
          <span className="sidebar-logo-text">MemoryLens</span>
        </div>
        
        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href || 
                             (item.href !== "/" && location.pathname.startsWith(item.href))
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`sidebar-link${isActive ? " active" : ""}`}
              >
                <item.icon size={18} />
                {item.name}
              </Link>
            )
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="status-dot"></div>
          <span>v2.1 • ACTIVE</span>
        </div>
      </aside>

      {/* Main Canvas */}
      <main className="main-content">
        <div className="page-container fade-in">
          {children}
        </div>
      </main>
    </div>
  )
}
