import { Link, Navigate, useNavigate } from 'react-router-dom'
import { IconBell } from './icons.jsx'

export function SiteHeader() {
  const navigate = useNavigate()

  return (
    <header className="st-header">
      <Link to="/ratings" className="st-header__logo">
        <img src="/sharetrajet-logo-v2.png" alt="ShareTrajet" className="st-header__logo-image" />
      </Link>
      <div className="st-header__actions">
        <button type="button" className="st-btn st-btn--primary" onClick={() => navigate('/signup')}>
          Sign up
        </button>
        <button type="button" className="st-btn st-btn--ghost" onClick={() => navigate('/signin')}>
          Sign in
        </button>
        <button type="button" className="st-icon-btn"  onClick={() => navigate('/notifications')}>
          <IconBell />
        </button>
      </div>
    </header>
  )
}