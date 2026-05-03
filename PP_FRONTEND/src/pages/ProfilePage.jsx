import { useState, useRef } from 'react'
import '../styles/profile.css'
export function ProfilePage() {
  const [role, setRole] = useState('passenger')
  const [photo, setPhoto] = useState(null)
  const [showModify, setShowModify] = useState(false)
  const fileInputRef = useRef(null)

  function handlePhotoChange(e) {
    const file = e.target.files[0]
    if (file) {
      const url = URL.createObjectURL(file)
      setPhoto(url)
      setShowModify(false)
    }
  }

  return (
    <div className="st-profile">

      {/* Modify Modal */}
      {showModify && (
        <div className="st-modal-overlay">
          <div className="st-modal" style={{ position: 'relative' }}>
            <button
              onClick={() => setShowModify(false)}
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
              Modify Profile Photo
            </p>
            <div className="st-modal__actions" style={{ justifyContent: 'center' }}>
              <button
                className="st-btn st-btn--primary"
                onClick={() => fileInputRef.current.click()}
              >
                Choose from Gallery
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={handlePhotoChange}
              />
            </div>
          </div>
        </div>
      )}

      {/* Profile Card */}
      <div className="st-profile__card">

        {/* Avatar */}
        <div className="st-profile__avatar-wrap">
          {photo ? (
            <img src={photo} alt="profile" className="st-profile__avatar-img" />
          ) : (
            <div className="st-profile__avatar-placeholder">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="8" r="4"/>
                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
              </svg>
            </div>
          )}
        </div>

        {/* Name */}
        <h2 className="st-profile__name">Oudjane Anias</h2>

        {/* Stats Row */}
        <div className="st-profile__stats">
          <div className="st-profile__stat">
            <span className="st-profile__stat-value">
              <span style={{ color: '#f59e0b' }}>★</span> 0.00
            </span>
            <span className="st-profile__stat-label">RATING</span>
          </div>
          <div className="st-profile__stat">
            <span className="st-profile__stat-value">0</span>
            <span className="st-profile__stat-label">RIDES</span>
          </div>

          {/* Role Toggle */}
          <div className="st-profile__roles">
            <button
              className={`st-role-btn ${role === 'passenger' ? 'st-role-btn--active-passenger' : ''}`}
              onClick={() => setRole('passenger')}
            >
              PASSENGER
            </button>
            <button
              className={`st-role-btn ${role === 'driver' ? 'st-role-btn--active-driver' : ''}`}
              onClick={() => setRole('driver')}
            >
              DRIVER
            </button>
          </div>
        </div>

        {/* Modify Button */}
        <button
          className="st-btn st-btn--primary"
          style={{ marginTop: '1rem', width: 'fit-content' }}
          onClick={() => setShowModify(true)}
        >
          MODIFY THE PROFILE
        </button>

        {/* About */}
        <div className="st-profile__about">
          <h3>About</h3>
        </div>

        {/* Contact */}
        <div className="st-profile__contact">
          <h3 style={{ color: 'var(--st-navy)', fontWeight: 700 }}>Contact Information</h3>

          <div className="st-profile__contact-item">
            <div className="st-profile__contact-icon" style={{ background: '#dbeafe' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="M2 7l10 7 10-7"/>
              </svg>
            </div>
            <div>
              <span className="st-profile__contact-label">EMAIL</span>
              <span className="st-profile__contact-value">a_oudjane@estin.dz</span>
            </div>
          </div>

          <div className="st-profile__contact-item">
            <div className="st-profile__contact-icon" style={{ background: '#dcfce7' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.79 19.79 0 0 1 11.61 19a19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 3.09 4.18 2 2 0 0 1 5.08 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L9.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
            </div>
            <div>
              <span className="st-profile__contact-label">PHONE</span>
              <span className="st-profile__contact-value">0655472942</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}