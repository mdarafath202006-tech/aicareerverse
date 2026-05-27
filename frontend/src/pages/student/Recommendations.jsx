/**
 * pages/student/Recommendations.jsx — AI Mentor Recommendations
 */
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { RiBrainLine, RiSparklingLine, RiSearchLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import MentorCard from "../../components/MentorCard";
import api from "../../api/client";
import toast from "react-hot-toast";

export default function Recommendations() {
  const [ranked, setRanked]     = useState([]);
  const [loading, setLoading]   = useState(true);
  const [requesting, setReq]    = useState(null);
  const [showModal, setModal]   = useState(null);
  const [message, setMessage]   = useState("");
  const [filter, setFilter]     = useState("");

  useEffect(() => {
    api.get("/recommendations")
      .then(r => setRanked(r.data.recommendations || []))
      .catch(() => toast.error("Could not load recommendations"))
      .finally(() => setLoading(false));
  }, []);

  const handleRequest = async () => {
    if (!showModal) return;
    setReq(showModal.alumni_id);
    try {
      const form = new FormData();
      form.append("message", message);
      const res = await fetch(`/student/request_mentor/${showModal.alumni_id}`, { method: "POST", body: form });
      if (res.ok || res.redirected) {
        toast.success("Mentorship request sent!");
        setModal(null);
        setMessage("");
      } else {
        toast.error("Failed to send request.");
      }
    } catch {
      toast.error("Network error");
    } finally {
      setReq(null);
    }
  };

  const filtered = filter
    ? ranked.filter(r =>
        r.name?.toLowerCase().includes(filter.toLowerCase()) ||
        r.job_role?.toLowerCase().includes(filter.toLowerCase()) ||
        r.company?.toLowerCase().includes(filter.toLowerCase())
      )
    : ranked;

  return (
    <Layout>
      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-8 h-8 rounded-xl bg-brand-500/15 flex items-center justify-center">
              <RiBrainLine className="text-brand-300" />
            </div>
            <h1 className="font-display font-bold text-2xl text-white">AI Mentor Recommendations</h1>
          </div>
          <p className="text-slate-400 text-sm ml-11">
            Ranked by semantic similarity · skill overlap · industry alignment
          </p>
        </motion.div>

        {/* Search filter */}
        <div className="relative max-w-sm">
          <RiSearchLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="input pl-10"
            placeholder="Filter by name, role, company..."
          />
        </div>

        {/* AI info banner */}
        <motion.div
          initial={{ opacity:0 }}
          animate={{ opacity:1 }}
          transition={{ delay: 0.2 }}
          className="flex items-start gap-3 p-4 rounded-xl bg-brand-500/5 border border-brand-500/20"
        >
          <RiSparklingLine className="text-brand-300 text-lg flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-display font-medium text-brand-200">Semantic AI Matching Active</p>
            <p className="text-xs text-slate-400 mt-0.5">
              Using sentence embeddings to match your skills profile with alumni expertise — not just keywords.
            </p>
          </div>
        </motion.div>

        {/* Cards grid */}
        {loading ? (
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="card p-5 space-y-4">
                <div className="flex gap-3">
                  <div className="w-12 h-12 skeleton rounded-2xl" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 skeleton w-3/4 rounded" />
                    <div className="h-3 skeleton w-1/2 rounded" />
                  </div>
                </div>
                <div className="h-2 skeleton rounded" />
                <div className="h-8 skeleton rounded-xl" />
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="card p-12 text-center">
            <RiBrainLine className="text-slate-600 text-4xl mx-auto mb-4" />
            <p className="text-slate-400">No mentors found. Update your profile with skills and interests.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
            {filtered.map((rec, i) => (
              <MentorCard
                key={rec.alumni_id}
                alumni={{ ...rec, id: rec.alumni_id }}
                percent={rec.percent}
                matchedSkills={rec.matched_skills}
                delay={i * 0.05}
                onRequest={(a) => setModal(a)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Request Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity:0, scale:0.95 }}
            animate={{ opacity:1, scale:1 }}
            className="card w-full max-w-md p-6 border-dark-500"
          >
            <h3 className="font-display font-bold text-white mb-1">Request Mentorship</h3>
            <p className="text-sm text-slate-400 mb-4">
              Sending request to <span className="text-brand-300">{showModal.name}</span>
            </p>
            <textarea
              value={message}
              onChange={e => setMessage(e.target.value)}
              className="input h-28 resize-none"
              placeholder="Introduce yourself and explain what you're hoping to learn..."
              maxLength={500}
            />
            <p className="text-xs text-slate-600 text-right mt-1">{message.length}/500</p>
            <div className="flex gap-3 mt-4">
              <button onClick={() => setModal(null)} className="btn-secondary flex-1 justify-center">Cancel</button>
              <button
                onClick={handleRequest}
                disabled={!!requesting}
                className="btn-primary flex-1 justify-center"
              >
                {requesting ? "Sending..." : "Send Request"}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </Layout>
  );
}
