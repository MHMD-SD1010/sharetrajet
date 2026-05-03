import { NavLink } from 'react-router-dom'
import { IconHome, IconMessage, IconSearch, IconSettings, IconStar, IconVerified } from './icons.jsx'

const linkClass = ({ isActive }) =>
  'st-navlink' + (isActive ? ' st-navlink--active' : '')

export function Sidebar() {
  return (
    <aside className="st-sidebar" aria-label="Main navigation">
      <nav className="st-sidebar__nav">
        <NavLink to="/profile" className={linkClass}>
          <IconHome />
          Profile
        </NavLink>
        <NavLink to="/messages" className={linkClass}>
          <IconMessage />
          Messages
        </NavLink>
        <NavLink to="/settings" className={linkClass}>
          <IconSettings />
          Settings
        </NavLink>
        <NavLink to="/preferences" className={linkClass}>
          <IconSearch />
          Preferences
        </NavLink>
        <NavLink to="/verified" className={linkClass}>
          <IconVerified />
          Verified Dashboard
        </NavLink>
        <NavLink to="/ratings" className={linkClass} end>
          <IconStar />
          Ratings and reviews
        </NavLink>
      </nav>
    </aside>
  )
}
