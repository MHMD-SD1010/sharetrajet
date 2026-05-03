import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

export function CommentPage() {
  const [text, setText] = useState('')
  const navigate = useNavigate()

  function handleSubmit(e) {
    e.preventDefault()
    navigate('/ratings')
  }

  return (
    <div className="st-comment-page">
      <h1 className="st-page-title">Add a comment</h1>
      <p style={{ margin: '0 0 1rem', color: 'var(--st-muted)', maxWidth: '36rem' }}>
        Share feedback about your trip. Your comment is sent to our trust and safety team and helps keep
        ShareTrajet reliable for everyone.
      </p>
      <form onSubmit={handleSubmit}>
        <label htmlFor="comment-body">Your comment</label>
        <textarea
          id="comment-body"
          name="comment"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="How was your ride?"
          required
        />
        <div className="st-comment-actions">
          <Link to="/ratings" className="st-btn st-btn--ghost" style={{ textDecoration: 'none' }}>
            Cancel
          </Link>
          <button type="submit" className="st-btn st-btn--comment">
            Done
          </button>
        </div>
      </form>
    </div>
  )
}
