import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/publish.css";

function Publish() {
  const [seats, setSeats] = useState(3);
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [showPopup, setShowPopup] = useState(false);


  const [distance, setDistance] = useState("");
  const [duration, setDuration] = useState("");

  const navigate = useNavigate();

  const cities = {
    alger: { lat: 36.75, lon: 3.06 },
    constantine: { lat: 36.36, lon: 6.61 },
    oran: { lat: 35.69, lon: -0.63 },
    setif: { lat: 36.19, lon: 5.41 },
    annaba: { lat: 36.9, lon: 7.76 }
    
   
  };

  const getDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;

    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(lat1 * Math.PI / 180) *
      Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) ** 2;

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const calculateTrip = (dep, arr) => {
    const d = cities[dep];
    const a = cities[arr];

    if (!d || !a) {
      setDistance("---- km");
      setDuration("--:--");
      return;
    }

    const dist = Math.floor(getDistance(d.lat, d.lon, a.lat, a.lon));
    const time = (dist / 80).toFixed(1);

    setDistance(dist + " km");
    setDuration(time + " h");
  };

  useEffect(() => {
    calculateTrip(departure, arrival);
  }, [departure, arrival]);

  return (
    <div className="publish-page">
      {showPopup && (
        <div className="publish-popup">
          <div className="publish-popup-content">
            <h1>Thank You!</h1>
            <p>Publishing your ride has been accepted </p>
            <button onClick={() => setShowPopup(false)}>Close</button>
          </div>
        </div>
      )}

      {/* Navbar */}
      <div className="navbar">
 
        {/* Logo */}
        <div className="nav-logo">
          <img src="/public/sharetrajet-logo-v2.png" alt="ShareTrajet logo" className="nav-logo-img" />
        
        </div>
 
        {/* Center links */}
        <div className="nav-links">
          <div className="btn-active">publish</div>
          <div onClick={() => navigate('../tripdetails')}>trips details</div>
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
 
      <div className="publish-container">

        <div className="publish-left">
          <h1>Publish a Ride</h1>
          <p>Share your journey, save money and meet new people.</p>

          <div className="publish-route">
            <svg width="30" height="30" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 14 L22 8 L38 14 L54 8 L54 46 L38 52 L22 46 L6 52 Z" 
        stroke="#3b3bdb" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" fill="white"/>
  <line x1="22" y1="8" x2="22" y2="46" stroke="#3b3bdb" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="38" y1="14" x2="38" y2="52" stroke="#3b3bdb" stroke-width="3.5" stroke-linecap="round"/>
</svg>
            <span>ROUTE</span>
          </div>

          <h6>DEPARTURE</h6>
          <input
            
            className="publish-input-icon"
            value={departure}
            onChange={(e) => setDeparture(e.target.value.toLowerCase())}
          />

          <h6>ARRIVAL</h6>
          <input
            className="publish-input-icon"
            value={arrival}
            onChange={(e) => setArrival(e.target.value.toLowerCase())}
          />

          <div className="publish-info-box">
            <p>{distance || "---- km"}</p>
            <p>Driving time: {duration || "--:--"}</p>
          </div>

          <div className="publish-warning">
            1 stop included <br />
            Total duration: {duration || "--:--"}
          </div>

          <div className="publish-calan">
            <svg width="40" height="40" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="12" width="48" height="42" rx="8" ry="8"
        stroke="url(#calGrad)" stroke-width="3.5" fill="white"/>
  <line x1="6" y1="26" x2="54" y2="26" stroke="url(#calGrad)" stroke-width="3.5"/>
  <line x1="20" y1="6" x2="20" y2="18" stroke="url(#calGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="40" y1="6" x2="40" y2="18" stroke="url(#calGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <defs>
    <linearGradient id="calGrad" x1="6" y1="6" x2="54" y2="54" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3b3bdb"/>
      <stop offset="100%" stop-color="#1a0080"/>
    </linearGradient>
  </defs>
</svg>
            <span> Date and Seat </span>
          </div>

          <h5>DEPARTURE DATE</h5>
          <input type="datetime-local" />

          <h5>AVAILABLE SEATS</h5>
          <div className="publish-seats">
            <button onClick={() => seats > 1 && setSeats(seats - 1)}>-</button>
            <span>{seats}</span>
            <button onClick={() => setSeats(seats + 1)}>+</button>
          </div>
        </div>

        <div className="publish-right">

          <div className="publish-trip-info">
            <h2>{distance || "---- km"} | {duration || "--:--"}</h2>
          </div>

          <div className="publish-map">
            <img src="/algeria.png" alt="Map of Algeria"/>
          </div>

          <h3>Ride Summary</h3>

          <p>🟢 {departure || "Departure"}</p>
          <p>🔴 {arrival || "Arrival"}</p>

          <div 
            className="publish-alert-toggle"
            onClick={() => setShowAlert(!showAlert)}
          >
            {showAlert ? "▼ Hide warning" : "▶ Show warning"}       
          </div>

          {showAlert && (
            <div className="publish-alert">
              Please check your car's fluids before long trips.
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#FF6B6B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          )}
          
           <button 
            className="publish-publish-btn"
            onClick={() => setShowPopup(true)}
          >
            Publish Ride →
          </button>

        </div>
      </div>
      <footer className="trip-footer">
        <button className="back-link-btn" onClick={() => navigate(-1)}>
          <span className="back-arrow">‹</span> Going back to offer a ride
        </button>
      </footer>
    </div>
  );
}

export default Publish;
