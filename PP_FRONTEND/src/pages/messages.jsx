import { useState } from 'react'
import '../styles/messages.css'

export function MessagesPage() {
  const [tab, setTab] = useState('private')
  const [selectedChat, setSelectedChat] = useState(null)

  const messages = [
    { id: 1, name: 'Leon S Kennedy', text: 'Are we still meeting at the gas station...', img: '/user.png' },
    { id: 2, name: 'Dante', text: "I've arrived at the pick-up point.", img: '/user.png' },
  ]

  const groups = [
    { id: 1, name: 'Raccoon city to silent hill', text: 'James: where could i find silent hill ?', img: '/redcar.png' },
    { id: 2, name: 'Silent hill Daily Commute', text: 'pyramid head posted a new schedule', img: '/bluenavigator.png' },
  ]

  return (
    <div className="messages-container">

      {!selectedChat && (
        <div className="messages-list">
          <div className="messages-tabs">
            <span className={tab === 'private' ? 'active' : ''} onClick={() => setTab('private')}>Private</span>
            <span className={tab === 'groups' ? 'active' : ''} onClick={() => setTab('groups')}>Groups</span>
          </div>

          {tab === 'private' && messages.map((m) => (
  <div key={m.id} className="message" onClick={() => setSelectedChat(m)}>
    <div className="st-avatar">{m.name[0]}</div>
    <div>
      <h4>{m.name}</h4>
      <p>{m.text}</p>
    </div>
  </div>
))}

          {tab === 'groups' && (
  <>
    <h3 className="group-title">ACTIVE CARPOOL GROUPS</h3>
    {groups.map((g) => (
      <div key={g.id} className="group" onClick={() => setSelectedChat(g)}>
        <div className="st-avatar">{g.name[0]}</div>
        <div>
          <h4>{g.name}</h4>
          <div className="group-users">
            <div className="st-avatar" style={{ width: 22, height: 22, fontSize: '0.6rem' }}>A</div>
            <div className="st-avatar" style={{ width: 22, height: 22, fontSize: '0.6rem' }}>B</div>
            <span>+2</span>
          </div>
          <p>{g.text}</p>
        </div>
      </div>
    ))}
  </>
)}
        </div>
      )}

      {selectedChat && (
        <div className="chat-full">
          <button className="back-btn" onClick={() => setSelectedChat(null)}>← Back</button>
          <h2>{selectedChat.name}</h2>
          <div className="chat-body">
            <div className="msg left">{selectedChat.text}</div>
            <div className="msg right">Hello 👋</div>
          </div>
          <div className="chat-input">
            <input placeholder="Type message..." />
            <button>➤</button>
          </div>
        </div>
      )}

    </div>
  )
}