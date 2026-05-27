/**
 * components/Layout.jsx — Main dashboard layout with animated sidebar
 */
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  RiDashboardLine, RiUserLine, RiSearchLine, RiBarChartLine,
  RiLightbulbLine, RiBrainLine, RiNotification3Line, RiLogoutBoxLine,
  RiMenuLine, RiCloseLine, RiGlobalLine, RiTeamLine,
} from "react-icons/ri";
import useStore from "../store/useStore";
import NotificationPanel from "./NotificationPanel";
import { useState } from "react";
import clsx from "clsx";

const studentNav = [
  { to: "/student/dashboard",       icon: RiDashboardLine, label: "Dashboard" },
  { to: "/student/recommendations", icon: RiBrainLine,     label: "AI Mentors" },
  { to: "/student/skill-gap",       icon: RiLightbulbLine, label: "Skill Gap" },
  { to: "/student/search",          icon: RiSearchLine,    label: "Search Alumni" },
  { to: "/student/profile",         icon: RiUserLine,      label: "My Profile" },
  { to: "/analytics",               icon: RiBarChartLine,  label: "Analytics" },
];

const alumniNav = [
  { to: "/alumni/dashboard", icon: RiDashboardLine, label: "Dashboard" },
  { to: "/alumni/profile",   icon: RiUserLine,      label: "My Profile" },
  { to: "/analytics",        icon: RiBarChartLine,  label: "Analytics" },
];

export default function Layout({ children }) {
  const { user, logout, sidebarOpen, toggleSidebar, unreadCount, onlineCount } = useStore();
  const location  = useLocation();
  const navigate  = useNavigate();
  const [showNotifs, setShowNotifs] = useState(false);

  const nav = user?.role === "alumni" ? alumniNav : studentNav;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="flex h-screen bg-dark-900 overflow-hidden">
      {/* ── Sidebar ─────────────────────────────────────────────── */}
      <AnimatePresence initial={false}>
        {sidebarOpen && (
          <motion.aside
            key="sidebar"
            initial={{ x: -280, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -280, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="w-64 flex-shrink-0 bg-dark-800 border-r border-dark-600 flex flex-col z-20"
          >
            {/* Logo */}
            <div className="p-6 border-b border-dark-600">
              <Link to="/" className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center shadow-glow-brand">
                  <RiBrainLine className="text-white text-xl" />
                </div>
                <div>
                  <div className="font-display font-bold text-white text-sm leading-none">AI CareerVerse</div>
                  <div className="text-[10px] text-slate-500 mt-0.5 uppercase tracking-wider">Career Intelligence</div>
                </div>
              </Link>
            </div>

            {/* User card */}
            <div className="p-4 border-b border-dark-600">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-dark-700">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                  {user?.name?.[0]?.toUpperCase() || "U"}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-display font-medium text-white truncate">{user?.name || "User"}</p>
                  <p className="text-[10px] text-slate-500 capitalize">{user?.role || "member"}</p>
                </div>
                <div className="ml-auto w-2 h-2 rounded-full bg-accent-green flex-shrink-0" title="Online" />
              </div>
            </div>

            {/* Nav links */}
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              <p className="text-[10px] text-slate-600 uppercase tracking-widest font-display mb-3 px-2">Navigation</p>
              {nav.map(({ to, icon: Icon, label }) => (
                <Link
                  key={to}
                  to={to}
                  className={clsx(
                    "sidebar-link",
                    location.pathname === to && "active"
                  )}
                >
                  <Icon className="text-lg flex-shrink-0" />
                  <span>{label}</span>
                </Link>
              ))}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-dark-600 space-y-1">
              <div className="flex items-center gap-2 px-4 py-2 text-xs text-slate-500">
                <RiGlobalLine />
                <span>{onlineCount} online</span>
              </div>
              <button onClick={handleLogout} className="sidebar-link w-full text-accent-rose hover:text-accent-rose hover:bg-accent-rose/5">
                <RiLogoutBoxLine className="text-lg" />
                <span>Sign Out</span>
              </button>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* ── Main ────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-14 bg-dark-800/80 backdrop-blur border-b border-dark-600 flex items-center px-4 gap-3 flex-shrink-0">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-dark-600 text-slate-400 hover:text-white transition-colors"
          >
            {sidebarOpen ? <RiCloseLine className="text-lg" /> : <RiMenuLine className="text-lg" />}
          </button>

          <div className="flex-1" />

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifs(!showNotifs)}
              className="relative p-2 rounded-lg hover:bg-dark-600 text-slate-400 hover:text-white transition-colors"
            >
              <RiNotification3Line className="text-lg" />
              {unreadCount > 0 && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-accent-rose rounded-full text-[10px] font-bold text-white flex items-center justify-center"
                >
                  {unreadCount > 9 ? "9+" : unreadCount}
                </motion.span>
              )}
            </button>
            <AnimatePresence>
              {showNotifs && (
                <NotificationPanel onClose={() => setShowNotifs(false)} />
              )}
            </AnimatePresence>
          </div>

          {/* Avatar */}
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center text-white font-bold text-xs">
            {user?.name?.[0]?.toUpperCase() || "U"}
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="h-full"
          >
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
}
