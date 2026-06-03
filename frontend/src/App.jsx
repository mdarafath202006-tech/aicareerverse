/**
 * App.jsx — Root component with routing
 */
import { Routes, Route, Navigate } from "react-router-dom";
import { useEffect } from "react";
import useStore from "./store/useStore";
import { useSocket } from "./hooks/useSocket";

// Pages
import LandingPage    from "./pages/Landing";
import LoginPage      from "./pages/Login";
import RegisterPage   from "./pages/Register";
import StudentDashboard from "./pages/student/Dashboard";
import Recommendations  from "./pages/student/Recommendations";
import SkillGap         from "./pages/student/SkillGap";
import StudentProfile   from "./pages/student/Profile";
import AlumniSearch     from "./pages/student/Search";
import AlumniDashboard  from "./pages/alumni/Dashboard";
import AlumniProfile    from "./pages/alumni/Profile";
import Analytics        from "./pages/Analytics";
import NotFound         from "./pages/NotFound";

function ProtectedRoute({ children, role }) {
  const { isLoggedIn, user } = useStore();
  if (!isLoggedIn) return <Navigate to="/login" replace />;
  if (role && user?.role !== role) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  const { darkMode, isLoggedIn, fetchNotifications } = useStore();
  useSocket(); // Initialize real-time connection

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  useEffect(() => {
    if (isLoggedIn) fetchNotifications();
  }, [isLoggedIn]);

  return (
    <Routes>
      <Route path="/"         element={<LandingPage />} />
      <Route path="/login"    element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Student routes */}
      <Route path="/student/dashboard" element={
        <ProtectedRoute role="student"><StudentDashboard /></ProtectedRoute>
      } />
      <Route path="/student/recommendations" element={
        <ProtectedRoute role="student"><Recommendations /></ProtectedRoute>
      } />
      <Route path="/student/skill-gap" element={
        <ProtectedRoute role="student"><SkillGap /></ProtectedRoute>
      } />
      <Route path="/student/profile" element={
        <ProtectedRoute role="student"><StudentProfile /></ProtectedRoute>
      } />
      <Route path="/student/search" element={
        <ProtectedRoute role="student"><AlumniSearch /></ProtectedRoute>
      } />

      {/* Alumni routes */}
      <Route path="/alumni/dashboard" element={
        <ProtectedRoute role="alumni"><AlumniDashboard /></ProtectedRoute>
      } />
      <Route path="/alumni/profile" element={
        <ProtectedRoute role="alumni"><AlumniProfile /></ProtectedRoute>
      } />

      {/* Shared */}
      <Route path="/analytics" element={
        <ProtectedRoute><Analytics /></ProtectedRoute>
      } />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
