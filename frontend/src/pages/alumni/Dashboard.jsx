/**
 * pages/alumni/Dashboard.jsx
 */
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { RiTeamLine, RiCheckLine, RiCloseLine, RiTimeLine, RiUserLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import StatCard from "../../components/StatCard";
import useStore from "../../store/useStore";
import toast from "react-hot-toast";

const statusBadge = {
  pending:  "badge-amber",
  accepted: "badge-green",
  rejected: "badge-rose",
};

export default function AlumniDashboard() {
  const { user } = useStore();
  const [requests, setRequests]   = useState([]);
  const [accepted, setAccepted]   = useState(0);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    // Load dashboard data (requests come from server-rendered page or API)
    fetch("/alumni/dashboard")
      .then(() => setLoading(false))
      .catch(() => setLoading(false));
  }, []);

  const respond = async (reqId, action) => {
    try {
      await fetch(`/alumni/respond/${reqId}/${action}`);
      setRequests(rs => rs.map(r => r.id === reqId ? { ...r, status: action === "accept" ? "accepted" : "rejected" } : r));
      if (action === "accept") {
        setAccepted(a => a + 1);
        toast.success("Mentorship accepted! 🎉");
      } else {
        toast("Request declined.");
      }
    } catch { toast.error("Action failed"); }
  };

  return (
    <Layout>
      <div className="p-6 max-w-5xl mx-auto space-y-6">
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}>
          <h1 className="font-display font-bold text-2xl text-white">
            Mentor Dashboard 👨‍🏫
          </h1>
          <p className="text-slate-400 text-sm mt-1">Manage mentorship requests and view your impact</p>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <StatCard icon={RiTeamLine}   label="Total Requests"    value={requests.length} color="brand"  delay={0} />
          <StatCard icon={RiCheckLine}  label="Active Mentorships" value={accepted}        color="green"  delay={0.05} />
          <StatCard icon={RiTimeLine}   label="Pending Reviews"    value={requests.filter(r=>r.status==="pending").length} color="amber" delay={0.1} />
        </div>

        {/* Quick links */}
        <div className="flex gap-3">
          <Link to="/alumni/profile" className="btn-secondary">
            <RiUserLine /> Edit Profile
          </Link>
          <Link to="/analytics" className="btn-secondary">
            View Analytics
          </Link>
        </div>

        {/* Requests */}
        <div>
          <h2 className="font-display font-semibold text-white text-sm mb-3 uppercase tracking-wider text-slate-400">
            Mentorship Requests
          </h2>
          {loading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => <div key={i} className="card p-5 h-24 skeleton" />)}
            </div>
          ) : requests.length === 0 ? (
            <div className="card p-12 text-center">
              <RiTeamLine className="text-slate-600 text-4xl mx-auto mb-3" />
              <p className="text-slate-400">No mentorship requests yet.</p>
              <p className="text-sm text-slate-500 mt-1">Complete your profile to attract students.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {requests.map((req, i) => (
                <motion.div
                  key={req.id}
                  initial={{ opacity:0, x:-16 }}
                  animate={{ opacity:1, x:0 }}
                  transition={{ delay: i * 0.05 }}
                  className="card p-5 flex items-start gap-4"
                >
                  <div className="w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center text-white font-bold flex-shrink-0">
                    {req.student_name?.[0]?.toUpperCase()}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className="font-display font-semibold text-white text-sm">{req.student_name}</p>
                      <span className={`badge ${statusBadge[req.status] || "badge-brand"}`}>{req.status}</span>
                      {req.department && <span className="text-xs text-slate-500">{req.department} · {req.year}</span>}
                    </div>
                    {req.message && (
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed line-clamp-2">{req.message}</p>
                    )}
                    {req.skills && (
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {req.skills.split(",").slice(0,3).map(s => (
                          <span key={s} className="badge-brand text-[10px]">{s.trim()}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  {req.status === "pending" && (
                    <div className="flex gap-2 flex-shrink-0">
                      <button onClick={() => respond(req.id, "accept")} className="btn-secondary btn-sm text-emerald-300 border-accent-green/20 hover:bg-accent-green/10">
                        <RiCheckLine /> Accept
                      </button>
                      <button onClick={() => respond(req.id, "reject")} className="btn-danger btn-sm">
                        <RiCloseLine />
                      </button>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
