import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/tripdetails.css';
 
const TripDetails = () => {
  const [showPopup, setShowPopup] = useState(false);
  const [seatCount, setSeatCount] = useState(1);
  const pricePerSeat = 200;
 
  const handleIncrement = () => {
    if (seatCount < 6) setSeatCount(seatCount + 1);
  };
  const handleDecrement = () => {
    if (seatCount > 1) setSeatCount(seatCount - 1);
  };
 
  const navigate = useNavigate();
 
  return (
    <div className="trip-container">
      {showPopup && (
        <div className="trip-popup">
          <div className="trip-popup-content">
            <h1>Thank You!</h1>
            <p>Booking accepted</p>
            <button onClick={() => setShowPopup(false)}>Close</button>
          </div>
        </div>
      )}
 
      {/* Navbar */}
      <div className="navbar">
 
        {/* Logo */}
        <div className="nav-logo">
          <img src="/sharetrajet-logo-v2.png" alt="ShareTrajet logo" className="nav-logo-img" />
         
        </div>
 
        {/* Center links */}
        <div className="nav-links">
          <div onClick={() => navigate('/')}>publish</div>
          <div className="btn-active">trips details</div>
          <div onClick={() => navigate('../resarvation')}>reservation</div>
        </div>
 
        {/* Right actions */}
        <div className="nav-buttons">
          <button className="btn-signup" onClick={() => navigate('/signup')}>Sign up</button>
          <button className="btn-login"  onClick={() => navigate('/signin')}>Sign in</button>
 
          {/* Notification bell */}
          <span className="icon" onClick={() => navigate('/notifications')}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" stroke="#3a86ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke="#3a86ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </span>
 
          {/* Messages */}
          <span className="icon" onClick={() => navigate('/messages')}>
            <svg fill="#3a86ff" width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M13 14h3.5c.827 0 1.5-.673 1.5-1.5v-9c0-.827-.673-1.5-1.5-1.5h-13C2.673 2 2 2.673 2 3.5V18l5.333-4H13zm-9-.1.154-.016L4 14v-.1z"/>
              <path d="M20.5 8H20V14.001c0 1.1-.893 1.993-1.99 1.999H8v.5c0 .827.673 1.5 1.5 1.5h7.167L22 22V9.5c0-.827-.673-1.5-1.5-1.5z"/>
            </svg>
          </span>
 
          {/* Profile */}
          <span className="icon" onClick={() => navigate('/profile')}>
            <svg fill="#3a86ff" width="20" height="20" viewBox="0 0 30.586 30.586" xmlns="http://www.w3.org/2000/svg">
              <g transform="translate(-546.269 -195.397)">
                <path d="M572.138,221.245a15.738,15.738,0 0,0-21.065-.253l-1.322-1.5a17.738,17.738,0 0,1 23.741.28Z"/>
                <path d="M561.464,204.152a4.96,4.96,0 1,1-4.96,4.96,4.966,4.966,0 0,1 4.96-4.96m0-2a6.96,6.96,0 1,0 6.96,6.96,6.96,6.96,0 0,0-6.96-6.96Z"/>
                <path d="M561.562,197.4a13.293,13.293,0 1,1-13.293,13.293A13.308,13.308,0 0,1 561.562,197.4m0-2a15.293,15.293,0 1,0 15.293,15.293A15.293,15.293,0 0,0 561.562,195.4Z"/>
              </g>
            </svg>
          </span>
        </div>
      </div>
 
      {/* Content grid */}
      <main className="trip-content-grid">
        <section className="trip-main-info">
          <h1 className="trip-header-title">
            Ride from Amizour, Béjaïa to <br />
            Iloula Oumalou, Tizi Ouzou
          </h1>
          <p className="trip-timestamp">Saturday, January 31, 2026 at 05:20:00</p>
 
          {/* Driver */}
          <div className="driver-profile">
            <div className="avatar-main">
              <div className="online-indicator"></div>
            </div>
            <div className="driver-details">
              <div className="driver-header">
                <h3>Saidi Mahmoud</h3>
                <span className="verified-label">VERIFIED</span>
              </div>
              <p className="driver-rating">⭐ 5.0 <span className="rides-count">(0 rides)</span></p>
              <p className="member-date">Member since December 2025</p>
            </div>
          </div>
 
          {/* Passengers */}
          <div className="confirmed-passengers-area">
            <h4>Confirmed Passengers (1)</h4>
            <div className="passenger-row-bg">
              <div className="avatar-small"></div>
              <div className="passenger-text">
                <p className="p-name">Hebib Kenza</p>
                <p className="p-seat">1 seat</p>
              </div>
            </div>
          </div>
 
          {/* Preferences */}
          <div className="preferences-area">
            <h2 className="pref-title">Driver Preferences</h2>
            <div className="tags-stack">
              <div className="tag-full blue-bg">Careful driver</div>
              <div className="tag-split-row">
                <div className="tag-half blue-bg">Fast driver</div>
                <div className="tag-half-long outline-bg">Smoking allowed</div>
              </div>
              <div className="tag-full blue-bg">With music</div>
              <div className="tag-full blue-bg">Chatty</div>
            </div>
          </div>
        </section>
 
        {/* Booking sidebar */}
        <aside className="trip-sidebar">
          <div className="booking-card">
            <div className="card-top">
              <div>
                <span className="price-label">PRICE PER SEAT</span>
                <p className="price-value">200 DA</p>
              </div>
              <span className="seats-remaining">2 available</span>
            </div>
 
            <div className="seat-counter">
              <button onClick={handleDecrement} className="counter-op">—</button>
              <span className="current-seats">{seatCount}</span>
              <button onClick={handleIncrement} className="counter-op">+</button>
            </div>
 
            <div className="total-display">
              Total: {seatCount * pricePerSeat} DA
            </div>
 
            <button className="book-btn" onClick={() => setShowPopup(true)}>
              Book Now
            </button>
          </div>
        </aside>
      </main>
 
      <footer className="trip-footer">
        <button className="back-link-btn" onClick={() => navigate(-1)}>
          <span className="back-arrow">‹</span> Going back to offer a ride
        </button>
      </footer>
    </div>
  );
};
 
export default TripDetails;
 