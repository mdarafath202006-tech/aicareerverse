/**
 * pages/student/Dashboard.jsx — Student Dashboard
 */
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  RiTeamLine, RiBrainLine, RiCheckLine, RiArrowRightLine,
  RiLightbulbLine, RiBarChartLine, RiSparklingLine,
} from "react-icons/ri";
import Layout from "../../components/Layout";
import StatCard from "../../components/StatCard";
import { TopSkillsChart } from "../../components/AnalyticsCharts";
import useStore from "../../store/useStore";
import api from "../../api/client";

const quickLinks = [
  { to: "/student/recommendations", icon: RiBrainLine,     color: "violet", label: "AI Mentor Match",   desc: "Find your ideal mentor" },
  { to: "/student/skill-gap",       icon: RiLightbulbLine, color: "amber",  label: "Skill Gap",         desc: "See what's missing" },
  { to: "/student/search",          icon: RiTeamLine,      color: "cyan",   label: "Browse Alumni",     desc: "Search by skill or company" },
  { to: "/analytics",               icon: RiBarChartLine,  color: "green",  label: "Career Analytics",  desc: "Market insights" },
];

export default function StudentDashboard() {
  const { user } = useStore();
  const [stats, setStats] = useState({ req_count: 0, accepted_count: 0, alumni_count: 0 });
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("/student/dashboard").then(r => r.text()),
      api.get("/analytics").catch(() => null),
    ]).then(([_, analyticsRes]) => {
      if (analyticsRes?.data) setAnalytics(analyticsRes.data);
      setLoading(false);
    });

    // Parse stats from meta tags injected by Flask (or fetch separately)
    const fetchStats = async () => {
      try {
        const r = await fetch("/api/analytics");
        // Stats come from template; for now use analytics data
      } catch (_) {}
    };
    fetchStats();
  }, []);

  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  return (
    <Layout>
      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-start justify-between"
        >
          <div>
            <h1 className="font-display font-bold text-2xl text-white">
              {greeting}, {user?.name?.split(" ")[0] || "there"} 👋
            </h1>
            <p className="text-slate-400 text-sm mt-1">Here's your career intelligence overview</p>
          </div>
          <Link to="/student/profile" className="btn-secondary btn-sm">
            Edit Profile
          </Link>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard icon={RiTeamLine}    label="Alumni Available"  value={analytics?.total_alumni || "—"} color="brand"  delay={0}    trend={12} />
          <StatCard icon={RiBrainLine}   label="AI Matches"        value="Top 10"                         color="violet" delay={0.05} />
          <StatCard icon={RiCheckLine}   label="Active Mentors"    value={stats.accepted_count}            color="green"  delay={0.1} />
          <StatCard icon={RiSparklingLine} label="AI Score"        value="—"                              color="amber"  delay={0.15} />
        </div>

        {/* Quick actions */}
        <div>
          <h2 className="font-display font-semibold text-white text-sm mb-3 uppercase tracking-wider text-slate-400">Quick Actions</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {quickLinks.map(({ to, icon: Icon, color, label, desc }, i) => {
              const colorMap = {
                violet: "from-accent-violet/20 to-accent-violet/5 border-accent-violet/20 text-violet-300",
                amber:  "from-accent-amber/20  to-accent-amber/5  border-accent-amber/20  text-amber-300",
                cyan:   "from-accent-cyan/20   to-accent-cyan/5   border-accent-cyan/20   text-cyan-300",
                green:  "from-accent-green/20  to-accent-green/5  border-accent-green/20  text-emerald-300",
              };
              return (
                <motion.div
                  key={to}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 + i * 0.05 }}
                  whileHover={{ y: -3 }}
                >
                  <Link
                    to={to}
                    className={`block p-4 rounded-2xl bg-gradient-to-b border ${colorMap[color]} transition-all duration-200 group`}
                  >
                    <Icon className="text-xl mb-3" />
                    <p className="font-display font-semibold text-white text-sm">{label}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{desc}</p>
                    <RiArrowRightLine className="text-slate-600 mt-3 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Charts row */}
        <div className="grid md:grid-cols-2 gap-6">
          {analytics?.top_skills ? (
            <TopSkillsChart data={analytics.top_skills} />
          ) : (
            <div className="card p-5">
              <div className="h-6 w-40 skeleton mb-4" />
              <div className="space-y-3">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="h-4 skeleton" style={{ width: `${80 - i * 12}%` }} />
                ))}
              </div>
            </div>
          )}

          {/* Activity feed */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="card p-5"
          >
            <h3 className="font-display font-semibold text-white text-sm mb-4">Getting Started</h3>
            <div className="space-y-3">
              {[
                { done: true,  label: "Created your account",           icon: "✅" },
                { done: false, label: "Complete your profile",           icon: "👤", to: "/student/profile" },
                { done: false, label: "Get AI mentor recommendations",   icon: "🤖", to: "/student/recommendations" },
                { done: false, label: "Run skill gap analysis",          icon: "📊", to: "/student/skill-gap" },
                { done: false, label: "Send first mentorship request",   icon: "📬" },
              ].map(({ done, label, icon, to }, i) => (
                <div key={i} className="flex items-center gap-3 text-sm">
                  <span className="text-base">{icon}</span>
                  {to ? (
                    <Link to={to} className={`flex-1 ${done ? "line-through text-slate-600" : "text-slate-300 hover:text-white"} transition-colors`}>
                      {label}
                    </Link>
                  ) : (
                    <span className={done ? "line-through text-slate-600 flex-1" : "text-slate-300 flex-1"}>{label}</span>
                  )}
                  {!done && to && <RiArrowRightLine className="text-slate-600 text-xs" />}
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </Layout>
  );
}
