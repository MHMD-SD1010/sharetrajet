import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { IconStar, IconTrendUp } from '../components/icons.jsx'
import { RatingModal } from '../components/RatingModal.jsx'
import '../styles/dashboard.css'
const DISTRIBUTION = [
  { stars: 5, count: 892 },
  { stars: 4, count: 215 },
  { stars: 3, count: 98 },
  { stars: 2, count: 11 },
  { stars: 1, count: 24 },
]

const REVIEWS = [
  {
    initials: 'AM',
    name: 'Ahmed Mansour',
    trip: 'Algiers → Oran',
    feedback: 'Smooth trip, on time and comfortable.',
    tone: 'good',
  },
  {
    initials: 'ZS',
    name: 'Zaidi Samira',
    trip: 'Oran → Algiers',
    feedback: 'Good driver — clear communication.',
    tone: 'mid',
  },
  {
    initials: 'KZ',
    name: 'Karim Ziani',
    trip: 'Constantine → Setif',
    feedback: 'Late pickup and noisy vehicle.',
    tone: 'bad',
  },
]

function StarRow({ value }) {
  const full = Math.floor(value)
  const half = value - full >= 0.5
  return (
    <div className="st-stars-row" aria-hidden>
      {[1, 2, 3, 4, 5].map((i) => {
        const filled = i <= full || (half && i === full + 1)
        return (
          <svg key={i} width="18" height="18" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
            <path
              fill={filled ? '#2563EB' : 'none'}
              stroke="#2563EB"
              strokeWidth="1.6"
              d="M12 2.5 14.9 9.5l7.6.6-5.8 4.7 1.9 7.4L12 17.9l-6.6 4.3 1.9-7.4L1.5 10.1l7.6-.6L12 2.5Z"
            />
          </svg>
        )
      })}
    </div>
  )
}

export function RatingsPage() {
  const [ratingOpen, setRatingOpen] = useState(false)
  const navigate = useNavigate()
  const maxCount = Math.max(...DISTRIBUTION.map((d) => d.count))

  function goComment() {
    navigate('/comment')
  }

  return (
    <>
      <h1 className="st-page-title">Ratings and reviews</h1>

      <section className="st-cards" aria-label="Summary">
        <button
          type="button"
          className="st-card st-clickable"
          onClick={() => setRatingOpen(true)}
          aria-label="Open rate your ride — average ratings"
        >
          <div className="st-card__label">Average ratings</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <IconStar style={{ color: '#2563EB', width: 22, height: 22 }} />
            <span className="st-pill">4.8 / 5.0</span>
          </div>
          <StarRow value={4.8} />
        </button>

        <div className="st-card">
          <div className="st-card__label">Total reviews</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <IconStar style={{ color: '#2563EB', width: 22, height: 22 }} />
            <span className="st-pill">1,240</span>
          </div>
          <p style={{ margin: '0.35rem 0 0', fontSize: '0.85rem', color: 'var(--st-muted)' }}>
            Verified platform users
          </p>
        </div>

        <div className="st-card">
          <div className="st-card__label">Critical reviews</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="st-pill st-pill--danger">24</span>
            <IconTrendUp style={{ color: 'var(--st-danger)' }} />
          </div>
          <p style={{ margin: '0.35rem 0 0', fontSize: '0.85rem', color: 'var(--st-danger)', fontWeight: 600 }}>
            Required attention
          </p>
        </div>
      </section>

      <div className="st-grid-2">
        <button
          type="button"
          className="st-panel st-clickable"
          onClick={() => setRatingOpen(true)}
          aria-label="Open rate your ride — rating breakdown"
          style={{ textAlign: 'left', border: 'none', padding: 0 }}
        >
          <div className="st-dist">
            <h2 className="st-dist__title">Rating breakdown</h2>
            {DISTRIBUTION.map((row) => (
              <div key={row.stars} className="st-dist__row">
                <span>{row.stars}</span>
                <div className="st-bar">
                  <div
                    className={
                      'st-bar__fill' + (row.stars === 1 ? ' st-bar__fill--critical' : '')
                    }
                    style={{ width: `${(row.count / maxCount) * 100}%` }}
                  />
                </div>
                <span className="st-count">{row.count}</span>
              </div>
            ))}
          </div>
        </button>

        <section className="st-panel" aria-label="Passenger feedback">
         
          <div
            className="st-feed st-clickable"
            role="link"
            tabIndex={0}
            onClick={goComment}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                goComment()
              }
            }}
            aria-label="Open comment page — passenger feedback"
          >
            <div className="st-feed__table-wrap">
              <table className="st-table">
                <thead>
                  <tr>
                    <th>User &amp; trip</th>
                    <th>Feedback</th>
                  </tr>
                </thead>
                <tbody>
                  {REVIEWS.map((r) => (
                    <tr key={r.name}>
                      <td>
                        <div className="st-user">
                          <div className="st-avatar">{r.initials}</div>
                          <div>
                            <div className="st-user__name">{r.name}</div>
                            <div className="st-user__trip">{r.trip}</div>
                          </div>
                        </div>
                      </td>
                      <td
                        className={
                          r.tone === 'good'
                            ? 'st-feedback--good'
                            : r.tone === 'mid'
                              ? 'st-feedback--mid'
                              : 'st-feedback--bad'
                        }
                      >
                        {r.feedback}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="st-pagination">
            <span>Showing 3 of 1,240 reviews</span>
            <button type="button" className="st-page-num" aria-label="Previous page">
              ‹
            </button>
            <button type="button" className="st-page-num st-page-num--current" aria-current="page">
              1
            </button>
            <button type="button" className="st-page-num">
              2
            </button>
            <button type="button" className="st-page-num">
              3
            </button>
            <button type="button" className="st-page-num" aria-label="Next page">
              ›
            </button>
          </div>
        </section>
      </div>

      <div className="st-actions-row">
        <button type="button" className="st-btn st-btn--rate" onClick={() => setRatingOpen(true)}>
          Rate your ride
        </button>
        <Link to="/comment" className="st-btn st-btn--comment" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center' }}>
          Add a comment
        </Link>
      </div>

      <RatingModal open={ratingOpen} onClose={() => setRatingOpen(false)} initialRating={5} />
    </>
  )
}
