import React, { useState } from "react";
import "../styles/notifications.css";
import { Link } from "react-router-dom";

const MessageIcon = () => (
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
    <path d="M3 7.2C3 6.07989 3 5.51984 3.21799 5.09202C3.40973 4.71569 3.71569 4.40973 4.09202 4.21799C4.51984 4 5.0799 4 6.2 4H17.8C18.9201 4 19.4802 4 19.908 4.21799C20.2843 4.40973 20.5903 4.71569 20.782 5.09202C21 5.51984 21 6.0799 21 7.2V20L17.6757 18.3378C17.4237 18.2118 17.2977 18.1488 17.1656 18.1044C17.0484 18.065 16.9277 18.0365 16.8052 18.0193C16.6672 18 16.5263 18 16.2446 18H6.2C5.07989 18 4.51984 18 4.09202 17.782C3.71569 17.5903 3.40973 17.2843 3.21799 16.908C3 16.4802 3 15.9201 3 14.8V7.2Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const EmailIcon = () => (
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
    <path d="M4 7.00005L10.2 11.65C11.2667 12.45 12.7333 12.45 13.8 11.65L20 7" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <rect x="3" y="5" width="18" height="14" rx="2" stroke="white" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

const CarIcon = () => (
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
    <path d="M3 8L5.72187 10.2682C5.90158 10.418 6.12811 10.5 6.36205 10.5H17.6379C17.8719 10.5 18.0984 10.418 18.2781 10.2682L21 8M6.5 14H6.51M17.5 14H17.51M8.16065 4.5H15.8394C16.5571 4.5 17.2198 4.88457 17.5758 5.50772L20.473 10.5777C20.8183 11.1821 21 11.8661 21 12.5623V18.5C21 19.0523 20.5523 19.5 20 19.5H19C18.4477 19.5 18 19.0523 18 18.5V17.5H6V18.5C6 19.0523 5.55228 19.5 5 19.5H4C3.44772 19.5 3 19.0523 3 18.5V12.5623C3 11.8661 3.18166 11.1821 3.52703 10.5777L6.42416 5.50772C6.78024 4.88457 7.44293 4.5 8.16065 4.5ZM7 14C7 14.2761 6.77614 14.5 6.5 14.5C6.22386 14.5 6 14.2761 6 14C6 13.7239 6.22386 13.5 6.5 13.5C6.77614 13.5 7 13.7239 7 14ZM18 14C18 14.2761 17.7761 14.5 17.5 14.5C17.2239 14.5 17 14.2761 17 14C17 13.7239 17.2239 13.5 17.5 13.5C17.7761 13.5 18 13.7239 18 14Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const TagIcon = () => (
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
    <path d="M8.5 3H11.5118C12.2455 3 12.6124 3 12.9577 3.08289C13.2638 3.15638 13.5564 3.27759 13.8249 3.44208C14.1276 3.6276 14.387 3.88703 14.9059 4.40589L20.5 10M7.5498 10.0498H7.5598M9.51178 6H8.3C6.61984 6 5.77976 6 5.13803 6.32698C4.57354 6.6146 4.1146 7.07354 3.82698 7.63803C3.5 8.27976 3.5 9.11984 3.5 10.8V12.0118C3.5 12.7455 3.5 13.1124 3.58289 13.4577C3.65638 13.7638 3.77759 14.0564 3.94208 14.3249C4.1276 14.6276 4.38703 14.887 4.90589 15.4059L8.10589 18.6059C9.29394 19.7939 9.88796 20.388 10.5729 20.6105C11.1755 20.8063 11.8245 20.8063 12.4271 20.6105C13.112 20.388 13.7061 19.7939 14.8941 18.6059L16.1059 17.3941C17.2939 16.2061 17.888 15.612 18.1105 14.9271C18.3063 14.3245 18.3063 13.6755 18.1105 13.0729C17.888 12.388 17.2939 11.7939 16.1059 10.6059L12.9059 7.40589C12.387 6.88703 12.1276 6.6276 11.8249 6.44208C11.5564 6.27759 11.2638 6.15638 10.9577 6.08289C10.6124 6 10.2455 6 9.51178 6ZM8.0498 10.0498C8.0498 10.3259 7.82595 10.5498 7.5498 10.5498C7.27366 10.5498 7.0498 10.3259 7.0498 10.0498C7.0498 9.77366 7.27366 9.5498 7.5498 9.5498C7.82595 9.5498 8.0498 9.77366 8.0498 10.0498Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const allNotifications = [
  {
    group: "TODAY",
    items: [
      { id: 1, icon: <MessageIcon />, title: "New Message", description: null, read: false },
      { id: 2, icon: <EmailIcon />, title: "Booking Request", description: "A passenger wants to join your ride to Downtown on Friday at 5:00PM.", read: false },
    ],
  },
  {
    group: "YESTERDAY",
    items: [
      { id: 3, icon: <CarIcon />, title: "Ride Completed", description: "How was your ride with arezki? Rate your experience now!", read: true },
      { id: 4, icon: <TagIcon />, title: "New Promo Code", description: 'Get 20% off your next 5 rides with code "COMMUTE20".', read: true },
    ],
  },
];

function Notifications() {
  const [activeTab, setActiveTab] = useState("all");

  const filteredGroups = allNotifications
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => activeTab === "all" ? true : !item.read),
    }))
    .filter((group) => group.items.length > 0);

  return (
    <div className="notif-page">

      {/* Header */}
      <div className="notif-header">
        <Link to="/" className="notif-back">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </Link>
        Notifications
      </div>

      {/* Tabs */}
      <div className="notif-tabs">
        <span
          className={activeTab === "all" ? "notif-active" : ""}
          onClick={() => setActiveTab("all")}
        >
          All
        </span>
        <span
          className={activeTab === "unread" ? "notif-active" : ""}
          onClick={() => setActiveTab("unread")}
        >
          Unread
        </span>
      </div>

      {/* Content */}
      <div className="notif-content">
        {filteredGroups.length === 0 ? (
          <p className="notif-empty">No notifications here.</p>
        ) : (
          filteredGroups.map((group) => (
            <div key={group.group}>
              <h2 className="notif-group-title">{group.group}</h2>
              {group.items.map((item) => (
                <div
                  key={item.id}
                  className={`notif-card ${item.read ? "notif-card-read" : "notif-card-unread"}`}
                >
                  <div className="notif-card-content">
                    <div className="notif-icon">{item.icon}</div>
                    <div className="notif-text">
                      <p className="notif-title">{item.title}</p>
                      {item.description && (
                        <p className="notif-description">{item.description}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ))
        )}
      </div>

    </div>
  );
}

export default Notifications;