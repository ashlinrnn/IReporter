import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { RecordsProvider } from './app/context/RecordsContext';
import Layout from './app/components/Layout';
import Login from './app/pages/Login';
import ForgotPassword from './app/pages/ForgotPassword';
import SignUp from './app/pages/SignUp';
import Home from './app/pages/Home';
import Activity from './app/pages/Activity';
import AdminDashboard from './app/pages/AdminDashboard';
import ReportSubmission from './app/pages/ReportSubmission';
import Settings from './app/pages/Settings';
import IncidentDetail from './app/pages/IncidentDetail';

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  if (!token) return <Navigate to="/login" />;
  if (adminOnly && !user.is_admin) return <Navigate to="/home" />;
  return children;
};

export default function App() {
  return (
    <BrowserRouter>
      <RecordsProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/home" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="report" element={<ReportSubmission />} />
            <Route path="activity" element={<Activity />} />
            <Route path="incident/:id" element={<IncidentDetail />} />
            <Route path="settings" element={<Settings />} />
            <Route path="admin" element={
              <ProtectedRoute adminOnly={true}>
                <AdminDashboard />
              </ProtectedRoute>
            } />
          </Route>
        </Routes>
      </RecordsProvider>
    </BrowserRouter>
  );
}