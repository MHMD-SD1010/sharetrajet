import { useState } from 'react'
import '../styles/settings.css'
export function SettingsPage() {
  const [showDeleteModal, setShowDeleteModal] = useState(false)

  function handleLogout() {
    localStorage.clear()
    sessionStorage.clear()
    window.location.href = '/'
  }

  function handleDeleteConfirm() {
    localStorage.clear()
    sessionStorage.clear()
    window.location.href = '/'
  }

  return (
    <div className="st-settings">

      {showDeleteModal && (
        <div className="st-modal-overlay">
          <div className="st-modal" style={{ position: 'relative' }}>

            <button
              onClick={() => setShowDeleteModal(false)}
              style={{
                position: 'absolute',
                top: '-0.5rem',
                right: '-0.5rem',
                background: 'white',
                border: '2px solid var(--st-navy)',
                borderRadius: '50%',
                width: '28px',
                height: '28px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                color: 'var(--st-navy)',
                fontWeight: 700,
                fontSize: '0.85rem',
              }}
            >
              ✕
            </button>

            <p className="st-modal__title" style={{ textAlign: 'center', fontSize: '1.2rem' }}>
              Are you sure you want to delete your account?
            </p>

            <div className="st-modal__actions" style={{ justifyContent: 'center' }}>
              <button className="st-btn--danger" onClick={handleDeleteConfirm}>Delete</button>
            </div>

          </div>
        </div>
      )}

      <div className="st-card-settings">
        <div className="st-card__left">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 11l4-4m0 0l4 4m-4-4v9"/>
            <path d="M21 13l-4 4m0 0l-4-4m4 4V8"/>
          </svg>
          <span style={{ color: 'white', fontWeight: 600 }}>Distance Unit (kilo/miles)</span>
        </div>
        <label className="st-toggle-switch">
          <input type="checkbox" />
          <span className="st-toggle-slider" />
        </label>
      </div>

      <div className="st-card-settings">
        <div className="st-card__left">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6l-1 14H6L5 6"/>
            <path d="M10 11v6"/>
            <path d="M14 11v6"/>
            <path d="M9 6V4h6v2"/>
          </svg>
          <span style={{ color: 'white', fontWeight: 600 }}>Delete Account</span>
        </div>
        <button className="st-btn--danger" onClick={() => setShowDeleteModal(true)}>Delete</button>
      </div>

      <div className="st-card-settings">
        <div className="st-card__left">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          <span style={{ color: 'white', fontWeight: 600 }}>Log out</span>
        </div>
        <button className="st-btn--danger" onClick={handleLogout}>Log out</button>
      </div>

    </div>
  )
}