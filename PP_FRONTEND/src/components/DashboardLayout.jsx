import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar.jsx'
import { SiteHeader } from './SiteHeader.jsx'
import '../styles/dashboard.css'

export function DashboardLayout() {
  return (
    <div className="st-shell">
      <Sidebar />
      <SiteHeader />
      <main className="st-main">
        <Outlet />
      </main>
    </div>
  )
}
