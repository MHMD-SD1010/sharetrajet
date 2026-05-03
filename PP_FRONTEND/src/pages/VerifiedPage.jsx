import '../styles/verified.css'
export function VerifiedPage() {
const stats = [
    { icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      ), label: 'Total Users', value: '12,480', change: '+12%', up: true },

    { icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 8L5.72187 10.2682C5.90158 10.418 6.12811 10.5 6.36205 10.5H17.6379C17.8719 10.5 18.0984 10.418 18.2781 10.2682L21 8M6.5 14H6.51M17.5 14H17.51M8.16065 4.5H15.8394C16.5571 4.5 17.2198 4.88457 17.5758 5.50772L20.473 10.5777C20.8183 11.1821 21 11.8661 21 12.5623V18.5C21 19.0523 20.5523 19.5 20 19.5H19C18.4477 19.5 18 19.0523 18 18.5V17.5H6V18.5C6 19.0523 5.55228 19.5 5 19.5H4C3.44772 19.5 3 19.0523 3 18.5V12.5623C3 11.8661 3.18166 11.1821 3.52703 10.5777L6.42416 5.50772C6.78024 4.88457 7.44293 4.5 8.16065 4.5ZM7 14C7 14.2761 6.77614 14.5 6.5 14.5C6.22386 14.5 6 14.2761 6 14C6 13.7239 6.22386 13.5 6.5 13.5C6.77614 13.5 7 13.7239 7 14ZM18 14C18 14.2761 17.7761 14.5 17.5 14.5C17.2239 14.5 17 14.2761 17 14C17 13.7239 17.2239 13.5 17.5 13.5C17.7761 13.5 18 13.7239 18 14Z"/>
        </svg>
      ), label: 'Active Rides', value: '342', change: '+5%', up: true },

    { icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
      ), label: 'Pending Docs', value: '12,480', change: '-2%', up: false },

    { icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
      ), label: 'Verified Users', value: '498', change: '+8%', up: true },
  ]

  const users = [
    { name: 'Amine Rahmani', email: 'amine.r@sharetrajet.dz', role: 'Driver', status: 'Active Now', date: 'May 24, 2024', action: 'Restore', actionColor: '#22c55e' },
    { name: 'Nora Hadid', email: 'Nora.h@sharetrajet.dz', role: 'Passenger', status: 'Active Now', date: 'May 11, 2024', action: 'Delete', actionColor: '#ef4444' },
    { name: 'Arezki Hebib', email: 'arezki.h@sharetrajet.dz', role: 'Driver', status: 'Active Now', date: 'July 10, 2025', action: 'Delete', actionColor: '#ef4444' },
  ]

  return (
    <div className="st-verified">

      <p className="st-verified__subtitle">PLATFORM OVERVIEW</p>
      <h1 className="st-page-title" style={{ marginBottom: '1.5rem' }}>Verified Dashboard</h1>

      {/* Stats */}
      <div className="st-verified__stats">
        {stats.map((s, i) => (
          <div key={i} className="st-verified__stat-card">
            <div className="st-verified__stat-icon">{s.icon}</div>
            <div>
              <span className={`st-verified__badge ${s.up ? 'st-verified__badge--up' : 'st-verified__badge--down'}`}>
                {s.up ? '↑' : '↓'} {s.change}
              </span>
              <p className="st-verified__stat-label">{s.label}</p>
              <p className="st-verified__stat-value">{s.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Table */}
      <h2 className="st-verified__table-title">Recent Users</h2>
      <div className="st-panel">
        <table className="st-table">
          <thead>
            <tr>
              <th>USER NAME</th>
              <th>ROLE</th>
              <th>STATUS</th>
              <th>DATE JOINED</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u, i) => (
              <tr key={i}>
                <td>
                  <div className="st-user">
                    <div className="st-avatar">{u.name[0]}</div>
                    <div>
                      <div className="st-user__name">{u.name}</div>
                      <div className="st-user__trip">{u.email}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span className="st-verified__role-badge" style={{
                    background: u.role === 'Driver' ? '#f97316' : '#3b82f6',
                  }}>
                    {u.role}
                  </span>
                </td>
                <td>
                  <span style={{ color: '#22c55e', fontWeight: 600 }}>● {u.status}</span>
                </td>
                <td style={{ color: 'var(--st-muted)' }}>{u.date}</td>
                <td>
                  <button className="st-verified__action-btn" style={{ background: u.actionColor }}>
                    {u.action}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Pagination */}
        <div className="st-verified__pagination">
          <span style={{ color: 'var(--st-blue)', fontWeight: 600 }}>Showing 3 of 248 recent users</span>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="st-verified__page-btn st-verified__page-btn--prev">Previous</button>
            <button className="st-verified__page-btn st-verified__page-btn--next">Next Page</button>
          </div>
        </div>
      </div>

    </div>
  )
}