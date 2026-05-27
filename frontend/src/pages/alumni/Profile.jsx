/**
 * pages/alumni/Profile.jsx
 */
import { useState } from "react";
import { motion } from "framer-motion";
import { RiUserLine, RiSaveLine, RiBriefcaseLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import useStore from "../../store/useStore";
import toast from "react-hot-toast";

export default function AlumniProfile() {
  const { user } = useStore();
  const [form, setForm] = useState({
    company: "", job_role: "", skills: "", location: "", linkedin: "", bio: "", is_hiring: false,
  });
  const [saving, setSaving] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const save = async () => {
    setSaving(true);
    try {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      await fetch("/alumni/profile", { method: "POST", body: fd });
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
            <h1 className="font-display font-bold text-2xl text-white">Alumni Profile</h1>
          </div>
        </motion.div>

        <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} transition={{ delay:0.1 }} className="card p-6 space-y-5">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-violet to-brand-600 flex items-center justify-center text-white font-bold text-2xl shadow-glow-brand">
              {user?.name?.[0]?.toUpperCase()}
            </div>
            <div>
              <p className="font-display font-bold text-white text-lg">{user?.name}</p>
              <p className="text-sm text-slate-400">Alumni Mentor</p>
            </div>
          </div>

          <div className="h-px bg-dark-500" />

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Company</label>
              <input type="text" value={form.company} onChange={set("company")} className="input" placeholder="Google, Meta, etc." />
            </div>
            <div>
              <label className="label">Job Role</label>
              <div className="relative">
                <RiBriefcaseLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input type="text" value={form.job_role} onChange={set("job_role")} className="input pl-10" placeholder="Software Engineer" />
              </div>
            </div>
          </div>

          <div>
            <label className="label">Skills</label>
            <textarea value={form.skills} onChange={set("skills")} className="input h-20 resize-none" placeholder="Python, React, System Design..." />
          </div>

          <div>
            <label className="label">Location</label>
            <input type="text" value={form.location} onChange={set("location")} className="input" placeholder="San Francisco, CA" />
          </div>

          <div>
            <label className="label">LinkedIn URL</label>
            <input type="url" value={form.linkedin} onChange={set("linkedin")} className="input" placeholder="https://linkedin.com/in/..." />
          </div>

          <div>
            <label className="label">Bio <span className="text-slate-600 normal-case tracking-normal">(max 1000 chars)</span></label>
            <textarea value={form.bio} onChange={set("bio")} className="input h-28 resize-none" placeholder="Share your journey and what you can offer as a mentor..." maxLength={1000} />
          </div>

          <div className="flex items-center gap-3 p-4 rounded-xl bg-dark-600 border border-dark-500">
            <input
              type="checkbox"
              id="is_hiring"
              checked={form.is_hiring}
              onChange={e => setForm(f => ({ ...f, is_hiring: e.target.checked }))}
              className="w-4 h-4 rounded accent-brand-500"
            />
            <label htmlFor="is_hiring" className="text-sm text-slate-300 cursor-pointer">
              My company is currently hiring — let students know!
            </label>
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
