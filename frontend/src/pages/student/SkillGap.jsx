/**
 * pages/student/SkillGap.jsx — Skill Gap Analysis
 */
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { RiLightbulbLine, RiCheckboxCircleLine, RiCloseCircleLine, RiExternalLinkLine, RiArrowRightLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import api from "../../api/client";
import toast from "react-hot-toast";

export default function SkillGap() {
  const [roles, setRoles]         = useState([]);
  const [selectedRole, setRole]   = useState("");
  const [gap, setGap]             = useState(null);
  const [loading, setLoading]     = useState(false);
  const [rolesLoading, setRL]     = useState(true);

  useEffect(() => {
    api.get("/analytics").then(r => {
      const roleData = r.data?.top_roles?.map(d => d.label) || [];
      setRoles(roleData);
    }).catch(() => {}).finally(() => setRL(false));
  }, []);

  const analyze = async () => {
    if (!selectedRole) return;
    setLoading(true);
    try {
      const r = await api.post("/skill-gap", { target_role: selectedRole });
      setGap(r.data);
    } catch {
      toast.error("Analysis failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const pct = gap?.coverage_pct ?? 0;
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <Layout>
      <div className="p-6 max-w-5xl mx-auto space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-8 h-8 rounded-xl bg-accent-amber/15 flex items-center justify-center">
              <RiLightbulbLine className="text-amber-300" />
            </div>
            <h1 className="font-display font-bold text-2xl text-white">Skill Gap Analysis</h1>
          </div>
          <p className="text-slate-400 text-sm ml-11">Compare your skills against what top companies require</p>
        </motion.div>

        {/* Role selector */}
        <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} transition={{ delay:0.1 }} className="card p-5">
          <label className="label">Target Job Role</label>
          <div className="flex gap-3">
            <select
              value={selectedRole}
              onChange={e => { setRole(e.target.value); setGap(null); }}
              className="input flex-1"
            >
              <option value="">Select a role to analyze...</option>
              {rolesLoading
                ? <option disabled>Loading roles...</option>
                : roles.map(r => <option key={r} value={r}>{r}</option>)
              }
            </select>
            <button
              onClick={analyze}
              disabled={!selectedRole || loading}
              className="btn-primary px-6"
            >
              {loading ? (
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
              ) : (
                <>Analyze <RiArrowRightLine /></>
              )}
            </button>
          </div>
        </motion.div>

        {/* Results */}
        <AnimatePresence>
          {gap && (
            <motion.div
              initial={{ opacity:0, y:20 }}
              animate={{ opacity:1, y:0 }}
              exit={{ opacity:0, y:-20 }}
              className="space-y-5"
            >
              {/* Score ring */}
              <div className="card p-6 flex items-center gap-8">
                <div className="relative flex-shrink-0">
                  <svg width="128" height="128" className="-rotate-90">
                    <circle cx="64" cy="64" r="54" fill="none" stroke="#172040" strokeWidth="12" />
                    <motion.circle
                      cx="64" cy="64" r="54"
                      fill="none"
                      stroke={pct >= 70 ? "#10b981" : pct >= 40 ? "#f59e0b" : "#f43f5e"}
                      strokeWidth="12"
                      strokeLinecap="round"
                      strokeDasharray={circumference}
                      initial={{ strokeDashoffset: circumference }}
                      animate={{ strokeDashoffset: offset }}
                      transition={{ duration: 1, ease: "easeOut" }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="font-display font-bold text-3xl text-white">{pct}%</span>
                    <span className="text-xs text-slate-500">coverage</span>
                  </div>
                </div>
                <div>
                  <h2 className="font-display font-bold text-xl text-white">{selectedRole}</h2>
                  <p className="text-sm text-slate-400 mt-1">
                    Based on <span className="text-white font-medium">{gap.role_count}</span> alumni in this role
                  </p>
                  <div className="flex items-center gap-4 mt-3 text-sm">
                    <div className="flex items-center gap-1.5 text-emerald-300">
                      <RiCheckboxCircleLine />
                      <span>{gap.student_has?.length || 0} skills matched</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-rose-300">
                      <RiCloseCircleLine />
                      <span>{gap.missing?.length || 0} skills missing</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Skills grid */}
              <div className="grid md:grid-cols-2 gap-5">
                {/* Have */}
                <div className="card p-5">
                  <h3 className="font-display font-semibold text-emerald-300 text-sm mb-3 flex items-center gap-2">
                    <RiCheckboxCircleLine /> Skills You Have ({gap.student_has?.length || 0})
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {gap.student_has?.length ? gap.student_has.map(sk => (
                      <span key={sk} className="badge-green">{sk}</span>
                    )) : <p className="text-xs text-slate-500">None matched yet — update your profile!</p>}
                  </div>
                </div>

                {/* Missing */}
                <div className="card p-5">
                  <h3 className="font-display font-semibold text-rose-300 text-sm mb-3 flex items-center gap-2">
                    <RiCloseCircleLine /> Skills to Learn ({gap.missing?.length || 0})
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {gap.missing?.length ? gap.missing.map(sk => (
                      <span key={sk} className="badge-rose">{sk}</span>
                    )) : <p className="text-xs text-emerald-400">🎉 You have all required skills!</p>}
                  </div>
                </div>
              </div>

              {/* Learning paths */}
              {gap.learning_paths && Object.keys(gap.learning_paths).length > 0 && (
                <div className="card p-5">
                  <h3 className="font-display font-semibold text-white text-sm mb-3">Recommended Learning Resources</h3>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {Object.entries(gap.learning_paths).map(([skill, url]) => (
                      <a
                        key={skill}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-3 rounded-xl bg-dark-600 border border-dark-500 hover:border-brand-500/40 transition-colors group"
                      >
                        <div className="w-8 h-8 rounded-lg bg-brand-500/10 flex items-center justify-center flex-shrink-0">
                          <RiLightbulbLine className="text-brand-300 text-sm" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-white font-display font-medium capitalize truncate">{skill}</p>
                          <p className="text-xs text-slate-500 truncate">{new URL(url).hostname}</p>
                        </div>
                        <RiExternalLinkLine className="text-slate-600 group-hover:text-brand-300 transition-colors flex-shrink-0" />
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
}
