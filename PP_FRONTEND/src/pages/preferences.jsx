import { useState } from 'react'
import '../styles/preference.css'

const IconSmoking = () => (
  <svg width="22" height="22" viewBox="0 0 128 128" fill="#0088FF" xmlns="http://www.w3.org/2000/svg">
    <rect x="14.1" y="84.1" width="83.7" height="14.8"/>
    <rect x="101.7" y="84.2" width="4.2" height="14.8"/>
    <rect x="109.6" y="84.2" width="4.2" height="14.8"/>
    <path d="M80.4,64.7c-6.4,0-11.6-5.2-11.6-11.5c0-1.2,0.2-2.4,0.5-3.5c-7.9-0.1-14.2-6.6-14.2-14.5c0-8,6.4-14.4,14.4-14.5v4.2c-5.6,0.1-10.2,4.7-10.2,10.4c0,5.7,4.7,10.4,10.4,10.4c0.7,0,1.4-0.1,2.1-0.2c0.2-0.1,0.4-0.1,0.6-0.1c1.3,0,2.5,1.1,2.5,2.4c0,0.5-0.2,1-0.4,1.4c-0.8,1.2-1.3,2.6-1.3,4.1c0,4,3.3,7.3,7.3,7.3h15.2c5.8,0,10.4,4.7,10.4,10.4l0,8.3h-4.2v-8.3c0-3.4-2.8-6.2-6.2-6.2H80.4z"/>
    <path d="M83.8,48.7c1.6-2,2.5-4.5,2.5-7.3c0-6.6-5.4-12-12-12h-0.9v-4.2h0.9c8.9,0,16.2,7.3,16.2,16.2c0,2.4-0.5,4.7-1.5,6.7l3,0c12.1,0,21.9,9.8,21.9,21.9v9.1h-4.2V70c0-9.8-7.9-17.7-17.7-17.7h-6.2c-1.3,0-2.4-1.1-2.4-2.4C83.4,49.5,83.6,49,83.8,48.7"/>
  </svg>
)

const IconMusic = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0088FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 19C9 20.1046 7.65685 21 6 21C4.34315 21 3 20.1046 3 19C3 17.8954 4.34315 17 6 17C7.65685 17 9 17.8954 9 19ZM9 19V5L21 3V17M21 17C21 18.1046 19.6569 19 18 19C16.3431 19 15 18.1046 15 17C15 15.8954 16.3431 15 18 15C19.6569 15 21 15.8954 21 17ZM9 9L21 7"/>
  </svg>
)

const IconPets = () => (
  <svg width="22" height="22" viewBox="0 0 20 20" fill="#0088FF" xmlns="http://www.w3.org/2000/svg">
    <path d="M11.9 8.4c1.3 0 2.1-1.9 2.1-3.1 0-1-.5-2.2-1.5-2.2-1.3 0-2.1 1.9-2.1 3.1 0 1 .5 2.2 1.5 2.2zm-3.8 0c1 0 1.5-1.2 1.5-2.2C9.6 4.9 8.8 3 7.5 3 6.5 3 6 4.2 6 5.2c-.1 1.3.7 3.2 2.1 3.2zm7.4-1c-1.3 0-2.2 1.8-2.2 3.1 0 .9.4 1.8 1.3 1.8 1.3 0 2.2-1.8 2.2-3.1 0-.9-.5-1.8-1.3-1.8zm-8.7 3.1c0-1.3-1-3.1-2.2-3.1-.9 0-1.3.9-1.3 1.8 0 1.3 1 3.1 2.2 3.1.9 0 1.3-.9 1.3-1.8zm3.2-.2c-2 0-4.7 3.2-4.7 5.4 0 1 .7 1.3 1.5 1.3 1.2 0 2.1-.8 3.2-.8 1 0 1.9.8 3 .8.8 0 1.7-.2 1.7-1.3 0-2.2-2.7-5.4-4.7-5.4z"/>
  </svg>
)

const IconConversation = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="#0088FF" xmlns="http://www.w3.org/2000/svg">
    <path d="M13 14h3.5c.827 0 1.5-.673 1.5-1.5v-9c0-.827-.673-1.5-1.5-1.5h-13C2.673 2 2 2.673 2 3.5V18l5.333-4H13zm-9-.1.154-.016L4 14v-.1z"/>
    <path d="M20.5 8H20V14.001c0 1.1-.893 1.993-1.99 1.999H8v.5c0 .827.673 1.5 1.5 1.5h7.167L22 22V9.5c0-.827-.673-1.5-1.5-1.5z"/>
  </svg>
)

const IconCar = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0088FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 8L5.72187 10.2682C5.90158 10.418 6.12811 10.5 6.36205 10.5H17.6379C17.8719 10.5 18.0984 10.418 18.2781 10.2682L21 8M6.5 14H6.51M17.5 14H17.51M8.16065 4.5H15.8394C16.5571 4.5 17.2198 4.88457 17.5758 5.50772L20.473 10.5777C20.8183 11.1821 21 11.8661 21 12.5623V18.5C21 19.0523 20.5523 19.5 20 19.5H19C18.4477 19.5 18 19.0523 18 18.5V17.5H6V18.5C6 19.0523 5.55228 19.5 5 19.5H4C3.44772 19.5 3 19.0523 3 18.5V12.5623C3 11.8661 3.18166 11.1821 3.52703 10.5777L6.42416 5.50772C6.78024 4.88457 7.44293 4.5 8.16065 4.5ZM7 14C7 14.2761 6.77614 14.5 6.5 14.5C6.22386 14.5 6 14.2761 6 14C6 13.7239 6.22386 13.5 6.5 13.5C6.77614 13.5 7 13.7239 7 14ZM18 14C18 14.2761 17.7761 14.5 17.5 14.5C17.2239 14.5 17 14.2761 17 14C17 13.7239 17.2239 13.5 17.5 13.5C17.7761 13.5 18 13.7239 18 14Z"/>
  </svg>
)

const IconBell = () => (
  <svg width="22" height="22" viewBox="0 0 32 32" fill="#0088FF" xmlns="http://www.w3.org/2000/svg">
    <path d="M29,25c-3,0-3-11-3-11c0-4.602-3.113-8.468-7.344-9.632C18.868,3.956,19,3.496,19,3c0-1.657-1.343-3-3-3s-3,1.343-3,3c0,0.496,0.132,0.956,0.344,1.368C9.113,5.532,6,9.398,6,14c0,0,0,11-3,11c-0.552,0-1,0.448-1,1c0,0.552,0.448,1,1,1h9.141C12.058,27.321,12,27.653,12,28c0,2.209,1.791,4,4,4s4-1.791,4-4c0-0.347-0.058-0.679-0.141-1H29c0.552,0,1-0.448,1-1C30,25.448,29.552,25,29,25z M15,3c0-0.551,0.449-1,1-1s1,0.449,1,1s-0.449,1-1,1S15,3.551,15,3z M8,14c0-4.411,3.589-8,8-8s8,3.589,8,8c0,0.118,0.004,2.919,0.393,5.77c0.07,0.513,0.184,1.33,0.392,2.23H7.214c0.208-0.9,0.322-1.717,0.392-2.23C7.996,16.919,8,14.118,8,14z M16,30c-1.103,0-2-0.897-2-2c0-0.136,0.025-0.294,0.078-0.499L14.466,26h3.067l0.389,1.501C17.975,27.706,18,27.864,18,28C18,29.103,17.103,30,16,30z M6.098,25c0.364-0.613,0.636-1.309,0.848-2h18.108c0.212,0.691,0.484,1.387,0.848,2H6.098z"/>
  </svg>
)

const IconEmail = () => (
  <svg width="22" height="22" viewBox="0 0 32 32" fill="none" stroke="#0088FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
    <polyline points="2,16 12,22 22,16"/>
    <path d="M18,11H6c-2.2,0-4,1.8-4,4v10c0,2.2,1.8,4,4,4h12c2.2,0,4-1.8,4-4V15C22,12.8,20.2,11,18,11z"/>
    <line x1="21.5" y1="13.1" x2="30" y2="8"/>
    <path d="M22,21h4c2.2,0,4-1.8,4-4V7c0-2.2-1.8-4-4-4H14c-2.2,0-4,1.8-4,4v4"/>
  </svg>
)

const IconSMS = () => (
  <svg width="22" height="22" viewBox="0 0 192 192" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path stroke="#0088FF" strokeLinejoin="round" strokeWidth="12" d="M30 54c0-13.255 10.745-24 24-24h84c13.255 0 24 10.745 24 24v84c0 13.255-10.745 24-24 24H30V54Z"/>
    <path stroke="#0088FF" strokeLinecap="round" strokeWidth="12" d="M54 96h84m-84 24h60M54 72h36"/>
  </svg>
)

const IconHide = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0088FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
    <path d="M3.99989 4L19.9999 20M16.4999 16.7559C15.1473 17.4845 13.6185 17.9999 11.9999 17.9999C8.46924 17.9999 5.36624 15.5478 3.5868 13.7788C3.1171 13.3119 2.88229 13.0784 2.7328 12.6201C2.62619 12.2933 2.62616 11.7066 2.7328 11.3797C2.88233 10.9215 3.11763 10.6875 3.58827 10.2197C4.48515 9.32821 5.71801 8.26359 7.17219 7.42676M19.4999 14.6335C19.8329 14.3405 20.138 14.0523 20.4117 13.7803L20.4146 13.7772C20.8832 13.3114 21.1182 13.0779 21.2674 12.6206C21.374 12.2938 21.3738 11.7068 21.2672 11.38C21.1178 10.9219 20.8827 10.6877 20.4133 10.2211C18.6338 8.45208 15.5305 6 11.9999 6C11.6624 6 11.3288 6.02241 10.9999 6.06448M13.3228 13.5C12.9702 13.8112 12.5071 14 11.9999 14C10.8953 14 9.99989 13.1046 9.99989 12C9.99989 11.4605 10.2135 10.9711 10.5608 10.6113"/>
  </svg>
)

const IconPeople = () => (
  <svg width="22" height="22" viewBox="0 0 600 600" fill="#0088FF" xmlns="http://www.w3.org/2000/svg">
    <path d="m 248.07279,-12.793664 c -72.13241,0 -131.33949,59.250935 -131.33949,131.392074 0,38.92115 17.25502,74.07152 44.45432,98.20884 C 58.500207,254.84854 -14.606185,358.21398 -14.606185,477.846 a 35.037921,35.037921 0 0 0 35.034809,35.03543 H 188.95771 c 6.88866,-25.46243 17.91968,-49.15043 32.45932,-70.0688 H 58.235927 C 73.730605,344.39181 153.38526,271.2598 248.07279,271.2598 c 13.12286,0 25.94065,1.45153 38.35524,4.13353 4.26325,-42.80875 34.59589,-78.30933 74.73011,-90.32371 11.57931,-19.5408 18.25414,-42.27592 18.25414,-66.47121 0,-72.141139 -59.20709,-131.392074 -131.33949,-131.392074 z m 0,70.068794 c 34.24293,0 61.26987,27.028459 61.26987,61.32328 0,34.29482 -27.02694,61.3274 -61.26987,61.3274 -34.24293,0 -61.27192,-27.03258 -61.27192,-61.3274 0,-34.294821 27.02899,-61.32328 61.27192,-61.32328 z"/>
    <path d="m 405.68024,197.47637 c -57.70598,0 -105.07159,47.40151 -105.07159,105.11449 0,31.13694 13.80343,59.25664 35.56289,78.56652 -82.15001,30.43306 -140.63449,113.12556 -140.63449,208.83127 a 28.030337,28.030337 0 0 0 28.0273,28.0278 h 182.11589 182.11452 a 28.030337,28.030337 0 0 0 28.0286,-28.0278 c 0,-95.70539 -58.4835,-178.39795 -140.63307,-208.83127 21.75947,-19.30988 35.56153,-47.42958 35.56153,-78.56652 0,-57.71298 -47.3656,-105.11449 -105.07158,-105.11449 z m 0,56.05559 c 27.39437,0 49.01562,21.62301 49.01562,49.0589 0,27.43588 -21.62125,49.06164 -49.01562,49.06164 -27.39437,0 -49.017,-21.62576 -49.017,-49.06164 0,-27.43589 21.62263,-49.0589 49.017,-49.0589 z m 0,171.18664 c 75.7501,0 139.47372,58.50552 151.86952,137.24226 H 405.68024 253.81075 C 266.2065,483.22412 329.93014,424.7186 405.68024,424.7186 Z"/>
  </svg>
)

export function PreferencesPage() {
  const [prefs, setPrefs] = useState({
    smoking: false,
    music: true,
    pets: false,
    pushNotif: false,
    emailAlerts: true,
    smsUpdates: true,
    hideProfile: false,
    mutualFriends: true
  })

  const [convLevel, setConvLevel] = useState('Quiet')
  const [driveLevel, setDriveLevel] = useState('Slow')

  const toggle = (key) => setPrefs({ ...prefs, [key]: !prefs[key] })

  return (
    <div className="pref-settings-card">

      <section className="pref-group">
        <h2 className="pref-section-title">CARPOOLING PREFERENCES</h2>

        <div className="pref-row">
          <span className="pref-row__label"><IconSmoking /> Smoking allowed</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.smoking} onChange={() => toggle('smoking')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-row">
          <span className="pref-row__label"><IconMusic /> Music preference</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.music} onChange={() => toggle('music')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-row">
          <span className="pref-row__label"><IconPets /> Pets allowed</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.pets} onChange={() => toggle('pets')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-segmented-box">
          <p className="pref-row__label"><IconConversation /> Conversation Level</p>
          <div className="pref-segmented-control">
            {['Quiet', 'Moderate', 'Chatty'].map(l => (
              <button key={l} className={convLevel === l ? 'active' : ''} onClick={() => setConvLevel(l)}>{l}</button>
            ))}
          </div>
        </div>

        <div className="pref-segmented-box">
          <p className="pref-row__label"><IconCar /> Driving Level</p>
          <div className="pref-segmented-control">
            {['Slow', 'Medium', 'Fast'].map(l => (
              <button key={l} className={driveLevel === l ? 'active' : ''} onClick={() => setDriveLevel(l)}>{l}</button>
            ))}
          </div>
        </div>
      </section>

      <section className="pref-group">
        <h2 className="pref-section-title">NOTIFICATION SETTINGS</h2>

        <div className="pref-row">
          <span className="pref-row__label"><IconBell /> Push notifications</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.pushNotif} onChange={() => toggle('pushNotif')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-row">
          <span className="pref-row__label"><IconEmail /> Email alerts</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.emailAlerts} onChange={() => toggle('emailAlerts')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-row">
          <span className="pref-row__label"><IconSMS /> SMS updates</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.smsUpdates} onChange={() => toggle('smsUpdates')} />
            <span className="pref-slider"></span>
          </label>
        </div>
      </section>

      <section className="pref-group">
        <h2 className="pref-section-title">ACCOUNT PRIVACY</h2>

        <div className="pref-row">
          <span className="pref-row__label"><IconHide /> Hide profile from search</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.hideProfile} onChange={() => toggle('hideProfile')} />
            <span className="pref-slider"></span>
          </label>
        </div>

        <div className="pref-row">
          <span className="pref-row__label"><IconPeople /> Show mutual friends only</span>
          <label className="pref-switch">
            <input type="checkbox" checked={prefs.mutualFriends} onChange={() => toggle('mutualFriends')} />
            <span className="pref-slider"></span>
          </label>
        </div>
      </section>

    </div>
  )
}