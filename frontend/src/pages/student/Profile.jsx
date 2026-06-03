/**
 * pages/student/Profile.jsx
 */
import { useState } from "react";
import { motion } from "framer-motion";
import { RiUserLine, RiSaveLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import useStore from "../../store/useStore";
import toast from "react-hot-toast";

export default function StudentProfile() {
  const { user } = useStore();
  const [form, setForm] = useState({ skills: "", interests: "", bio: "", github_url: "", linkedin_url: "" });
  const [saving, setSaving] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const save = async () => {
    setSaving(true);
    try {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      await fetch("/student/profile", { method: "POST", body: fd });
      toast.success("Profile updated!");
    } catch { toast.error("Failed to save."); }
    finally { setSaving(false); }
  };

  return (
    <Layout>
      <div className="p-6 max-w-2xl mx-auto space-y-5">
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-8 h-8 rounded-xl bg-brand-500/15 flex items-center justify-center">
              <RiUserLine className="text-brand-300" />
            </div>
            <h1 className="font-display font-bold text-2xl text-white">My Profile</h1>
          </div>
        </motion.div>

        <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} transition={{ delay:0.1 }} className="card p-6 space-y-5">
          {/* Avatar */}
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center text-white font-bold text-2xl shadow-glow-brand">
              {user?.name?.[0]?.toUpperCase()}
            </div>
            <div>
              <p className="font-display font-bold text-white text-lg">{user?.name}</p>
              <p className="text-sm text-slate-400 capitalize">{user?.role}</p>
            </div>
          </div>

          <div className="h-px bg-dark-500" />

          <div>
            <label className="label">Skills <span className="text-slate-600 normal-case tracking-normal">(comma separated)</span></label>
            <textarea value={form.skills} onChange={set("skills")} className="input h-20 resize-none" placeholder="Python, React, Machine Learning, SQL..." />
          </div>
          <div>
            <label className="label">Interests</label>
            <textarea value={form.interests} onChange={set("interests")} className="input h-20 resize-none" placeholder="AI, Web Development, Data Science..." />
          </div>
          <div>
            <label className="label">Bio <span className="text-slate-600 normal-case tracking-normal">(max 1000 chars)</span></label>
            <textarea value={form.bio} onChange={set("bio")} className="input h-28 resize-none" placeholder="Tell mentors about yourself..." maxLength={1000} />
            <p className="text-xs text-slate-600 text-right mt-1">{form.bio.length}/1000</p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">GitHub URL</label>
              <input type="url" value={form.github_url} onChange={set("github_url")} className="input" placeholder="https://github.com/..." />
            </div>
            <div>
              <label className="label">LinkedIn URL</label>
              <input type="url" value={form.linkedin_url} onChange={set("linkedin_url")} className="input" placeholder="https://linkedin.com/in/..." />
            </div>
          </div>
          <button onClick={save} disabled={saving} className="btn-primary w-full justify-center py-3">
            <RiSaveLine />
            {saving ? "Saving..." : "Save Profile"}
          </button>
        </motion.div>
      </div>
    </Layout>
  );
}
