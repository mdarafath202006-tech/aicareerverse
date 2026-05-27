/**
 * pages/Login.jsx — Animated login page
 */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { RiBrainLine, RiMailLine, RiLockLine, RiGoogleLine, RiLinkedinBoxLine, RiEyeLine, RiEyeOffLine } from "react-icons/ri";
import toast from "react-hot-toast";
import useStore from "../store/useStore";

export default function LoginPage() {
  const navigate  = useNavigate();
  const { setUser } = useStore();
  const [form, setForm] = useState({ email: "", password: "" });
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Login failed");
      setUser(data.user, data.access_token);
      toast.success(`Welcome back, ${data.user.name}!`);
      const role = data.user.role;
      navigate(role === "student" ? "/student/dashboard" : role === "alumni" ? "/alumni/dashboard" : "/");
    } catch (err) {
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-hero-gradient opacity-50" />
      <div className="absolute inset-0 bg-grid-pattern opacity-20" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center shadow-glow-brand">
              <RiBrainLine className="text-white text-2xl" />
            </div>
          </Link>
          <h1 className="font-display font-bold text-2xl text-white mt-4">Welcome back</h1>
          <p className="text-slate-400 text-sm mt-1">Sign in to your AI CareerVerse account</p>
        </div>

        <div className="card p-8 border-dark-500">
          {/* OAuth buttons */}
          <div className="grid grid-cols-2 gap-3 mb-6">
            <a href="/auth/google" className="btn-secondary justify-center py-2.5 text-sm">
              <RiGoogleLine className="text-rose-400 text-lg" />
              Google
            </a>
            <a href="/auth/linkedin" className="btn-secondary justify-center py-2.5 text-sm">
              <RiLinkedinBoxLine className="text-blue-400 text-lg" />
              LinkedIn
            </a>
          </div>

          <div className="relative flex items-center gap-3 mb-6">
            <div className="flex-1 h-px bg-dark-500" />
            <span className="text-xs text-slate-600 font-display">or continue with email</span>
            <div className="flex-1 h-px bg-dark-500" />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Email address</label>
              <div className="relative">
                <RiMailLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-lg" />
                <input
                  type="email"
                  value={form.email}
                  onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
                  className="input pl-10"
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="label">Password</label>
              <div className="relative">
                <RiLockLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-lg" />
                <input
                  type={showPw ? "text" : "password"}
                  value={form.password}
                  onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
                  className="input pl-10 pr-10"
                  placeholder="••••••••"
                  required
                />
                <button type="button" onClick={() => setShowPw(!showPw)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white transition-colors">
                  {showPw ? <RiEyeOffLine /> : <RiEyeLine />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full justify-center py-3 text-base mt-2"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                  </svg>
                  Signing in...
                </span>
              ) : "Sign In"}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Don't have an account?{" "}
            <Link to="/register" className="text-brand-300 hover:text-brand-200 font-display font-medium">
              Sign up free
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
