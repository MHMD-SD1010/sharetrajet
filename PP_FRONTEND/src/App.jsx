import { Navigate, Route, Routes } from 'react-router-dom';
import { DashboardLayout } from './components/DashboardLayout.jsx';
import { RatingsPage } from './pages/RatingsPage.jsx';
import { CommentPage } from './pages/CommentPage.jsx';
import { SettingsPage } from './pages/SettingsPage.jsx';
import { ProfilePage } from './pages/ProfilePage.jsx';
import { VerifiedPage } from './pages/VerifiedPage.jsx';
import { MessagesPage } from './pages/messages.jsx';
import { PreferencesPage } from './pages/preferences.jsx';
import Publish from './pages/publish.jsx';
import Signup from './pages/signup.jsx';
import Signin from './pages/signin.jsx';
import Notifications from './pages/notifications.jsx';
import TripDetails from './pages/tripdetails.jsx';

export default function App() {
  return (
    <Routes>
      {/* 1. AUTH ROUTES (No Dashboard Layout) */}
      <Route path="/signup" element={<Signup />} />
      <Route path="/signin" element={<Signin />} />

      {/* 2. DASHBOARD ROUTES (Wrapped in Layout) */}
      <Route element={<DashboardLayout />}>
        {/* Landing on "/" or "/dashboard" sends them to publish */}
        <Route path="/" element={<Navigate to="/publish" replace />} />
        <Route path="/dashboard" element={<Navigate to="/publish" replace />} />
        
      
        <Route path="/ratings" element={<RatingsPage />} />
        <Route path="/comment" element={<CommentPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/messages" element={<MessagesPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/preferences" element={<PreferencesPage />} />
        <Route path="/verified" element={<VerifiedPage />} />
     
        
      </Route>
      <Route path="/publish" element={<Publish />} />
<Route path="/tripdetails" element={<TripDetails />} />
<Route path="/notifications" element={<Notifications />} />
      {/* 3. FALLBACK */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}