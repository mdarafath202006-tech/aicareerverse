/**
 * pages/Register.jsx — Registration with role toggle
 */
import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { RiBrainLine, RiUserLine, RiMailLine, RiLockLine, RiTeamLine, RiGraduationCapLine } from "react-icons/ri";
import toast from "react-hot-toast";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [params]  = useSearchParams();
  const [role, setRole] = useState(params.get("role") || "student");
  const [loading, setLoading]  = useState(false);
  const [form, setForm] = useState({
    name: "", email: "", password: "",
    department: "", year: "",
    grad_year: "", company: "", job_role: "",
  });

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = new FormData();
      Object.entries({ ...form, role }).forEach(([k, v]) => payload.append(k, v));
      const res = await fetch("/register", { method: "POST", body: payload });
      const text = await res.text();
      if (res.redirected || res.ok) {
        toast.success("Account created! Please sign in.");
        navigate("/login");
      } else {
        toast.error("Registration failed. Check your inputs.");
      }
    } catch (err) {
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center p-4 py-12">
      <div className="absolute inset-0 bg-hero-gradient opacity-50" />
      <div className="absolute inset-0 bg-grid-pattern opacity-20" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative w-full max-w-md"
      >
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center shadow-glow-brand">
              <RiBrainLine className="text-white text-lg" />
            </div>
            <span className="font-display font-bold text-white">AI CareerVerse</span>
          </Link>
          <h1 className="font-display font-bold text-2xl text-white mt-4">Create your account</h1>
          <p className="text-slate-400 text-sm mt-1">Start your AI-powered career journey</p>
        </div>

        <div className="card p-8 border-dark-500">
          {/* Role toggle */}
          <div className="flex gap-2 p-1 bg-dark-600 rounded-xl mb-6">
            {["student", "alumni"].map(r => (
              <button
                key={r}
                type="button"
                onClick={() => setRole(r)}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-display font-medium transition-all duration-200 ${
                  role === r
                    ? "bg-brand-500 text-white shadow-glow-brand/30"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {r === "student" ? <RiGraduationCapLine /> : <RiTeamLine />}
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Common fields */}
            <div>
              <label className="label">Full Name</label>
              <div className="relative">
                <RiUserLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input type="text" value={form.name} onChange={set("name")} className="input pl-10" placeholder="Alex Johnson" required />
              </div>
            </div>
            <div>
              <label className="label">Email</label>
              <div className="relative">
                <RiMailLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input type="email" value={form.email} onChange={set("email")} className="input pl-10" placeholder="you@example.com" required />
              </div>
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <RiLockLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input type="password" value={form.password} onChange={set("password")} className="input pl-10" placeholder="Min 8 chars, 1 uppercase, 1 number" required />
              </div>
            </div>

            {/* Role-specific fields */}
            <AnimatePresence mode="wait">
              {role === "student" ? (
                <motion.div key="student" initial={{ opacity:0, height:0 }} animate={{ opacity:1, height:"auto" }} exit={{ opacity:0, height:0 }} className="space-y-4 overflow-hidden">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="label">Department</label>
                      <input type="text" value={form.department} onChange={set("department")} className="input" placeholder="CSE" />
                    </div>
                    <div>
                      <label className="label">Year</label>
                      <select value={form.year} onChange={set("year")} className="input">
                        <option value="">Select</option>
                        {["1st","2nd","3rd","4th","5th"].map(y => <option key={y}>{y}</option>)}
                      </select>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <motion.div key="alumni" initial={{ opacity:0, height:0 }} animate={{ opacity:1, height:"auto" }} exit={{ opacity:0, height:0 }} className="space-y-4 overflow-hidden">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="label">Graduation Year</label>
                      <input type="number" value={form.grad_year} onChange={set("grad_year")} className="input" placeholder="2022" min="2000" max="2030" />
                    </div>
                    <div>
                      <label className="label">Company</label>
                      <input type="text" value={form.company} onChange={set("company")} className="input" placeholder="Google" />
                    </div>
                  </div>
                  <div>
                    <label className="label">Job Role</label>
                    <input type="text" value={form.job_role} onChange={set("job_role")} className="input" placeholder="Software Engineer" />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <button type="submit" disabled={loading} className="btn-primary w-full justify-center py-3 text-base mt-2">
              {loading ? "Creating account..." : "Create Account"}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Already have an account?{" "}
            <Link to="/login" className="text-brand-300 hover:text-brand-200 font-display font-medium">Sign in</Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
