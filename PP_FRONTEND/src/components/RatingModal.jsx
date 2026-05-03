import { useEffect, useState } from 'react'

const LABELS = ['Poor', 'Fair', 'Okay', 'Good ride', 'Excellent ride !']

function Star({ filled, onClick, label }) {
  return (
    <button type="button" className="st-star-btn" onClick={onClick} aria-label={label}>
      <svg width="44" height="44" viewBox="0 0 24 24" aria-hidden>
        <path
          fill={filled ? '#2563EB' : 'none'}
          stroke="#2563EB"
          strokeWidth="1.8"
          d="M12 2.5 14.9 9.5l7.6.6-5.8 4.7 1.9 7.4L12 17.9l-6.6 4.3 1.9-7.4L1.5 10.1l7.6-.6L12 2.5Z"
        />
      </svg>
    </button>
  )
}

export function RatingModal({ open, onClose, initialRating = 5 }) {
  const [rating, setRating] = useState(initialRating)

  useEffect(() => {
    if (open) setRating(initialRating)
  }, [open, initialRating])

  useEffect(() => {
    if (!open) return
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  const title = LABELS[rating - 1] ?? 'Rate your ride'

  return (
    <div
      className="st-modal-overlay"
      role="presentation"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div className="st-modal" role="dialog" aria-modal="true" aria-labelledby="rating-modal-title">
        <h2 id="rating-modal-title" className="st-modal__title">
          {title}
        </h2>
        <div className="st-modal__stars">
          {[1, 2, 3, 4, 5].map((n) => (
            <Star
              key={n}
              filled={n <= rating}
              label={`${n} star${n > 1 ? 's' : ''}`}
              onClick={() => setRating(n)}
            />
          ))}
        </div>
        <div className="st-modal__actions">
          <button type="button" className="st-btn st-btn--done" onClick={onClose}>
            Done
          </button>
        </div>
      </div>
    </div>
  )
}
