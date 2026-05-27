/**
 * pages/Landing.jsx — Modern animated landing page
 */
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { RiBrainLine, RiSparklingLine, RiArrowRightLine, RiBarChartLine, RiTeamLine, RiLightbulbLine } from "react-icons/ri";

const features = [
  { icon: RiBrainLine,     color: "from-brand-500 to-blue-400",   title: "AI Mentor Matching",    desc: "Semantic embedding-based mentor recommendations that understand your skills deeply." },
  { icon: RiBarChartLine,  color: "from-accent-violet to-pink-500", title: "Career Analytics",    desc: "Real-time dashboards showing placement trends, skill demands, and company insights." },
  { icon: RiLightbulbLine, color: "from-accent-cyan to-teal-400",  title: "Skill Gap Analysis",  desc: "Know exactly what skills you need for your target role with learning path suggestions." },
  { icon: RiTeamLine,      color: "from-accent-amber to-orange-400", title: "Live Networking",   desc: "Real-time chat and mentorship connections with Socket.IO powered notifications." },
];

const stats = [
  { value: "500+", label: "Alumni Mentors" },
  { value: "95%",  label: "Match Accuracy" },
  { value: "2.4x", label: "Faster Placement" },
  { value: "10k+", label: "Students Helped" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-dark-900 text-white overflow-x-hidden">
      {/* Nav */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-dark-600 bg-dark-900/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center shadow-glow-brand">
              <RiBrainLine className="text-white text-lg" />
            </div>
            <span className="font-display font-bold text-white">AI CareerVerse</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login"    className="btn-ghost text-sm">Sign In</Link>
            <Link to="/register" className="btn-primary text-sm">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative min-h-screen flex items-center justify-center pt-16">
        {/* Background effects */}
        <div className="absolute inset-0 bg-grid-pattern opacity-30" />
        <div className="absolute inset-0 bg-hero-gradient" />

        {/* Floating orbs */}
        <motion.div
          animate={{ scale: [1, 1.1, 1], opacity: [0.2, 0.35, 0.2] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-brand-500/20 blur-3xl pointer-events-none"
        />
        <motion.div
          animate={{ scale: [1, 1.15, 1], opacity: [0.15, 0.3, 0.15] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
          className="absolute bottom-1/3 right-1/4 w-80 h-80 rounded-full bg-accent-violet/20 blur-3xl pointer-events-none"
        />

        <div className="relative z-10 text-center max-w-4xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-brand-500/30 bg-brand-500/10 text-brand-300 text-xs font-display font-medium mb-8"
          >
            <RiSparklingLine />
            AI-Powered Career Intelligence Platform
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="font-display font-bold text-5xl md:text-7xl leading-tight mb-6"
          >
            Your Career,{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-accent-cyan to-accent-violet">
              Supercharged
            </span>{" "}
            by AI
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Connect with the perfect alumni mentor using semantic AI matching. Analyze your skill gaps,
            track placement trends, and accelerate your career journey.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center gap-4 justify-center"
          >
            <Link to="/register" className="btn-primary px-8 py-3.5 text-base shadow-glow-brand">
              Start for Free
              <RiArrowRightLine className="text-xl" />
            </Link>
            <Link to="/login" className="btn-secondary px-8 py-3.5 text-base">
              Sign In
            </Link>
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
        >
          <div className="w-px h-12 bg-gradient-to-b from-brand-500/60 to-transparent" />
        </motion.div>
      </section>

      {/* Stats */}
      <section className="py-20 border-y border-dark-600 bg-dark-800/50">
        <div className="max-w-4xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map(({ value, label }, i) => (
              <motion.div
                key={label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <p className="font-display font-bold text-4xl text-white mb-1">{value}</p>
                <p className="text-sm text-slate-500 uppercase tracking-wider font-display">{label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 max-w-6xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="font-display font-bold text-4xl text-white mb-4">
            Everything you need to{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-accent-cyan">
              grow faster
            </span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">Built for students who want to make smarter career decisions backed by real alumni data and AI.</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          {features.map(({ icon: Icon, color, title, desc }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              whileHover={{ y: -4 }}
              className="card-hover p-6 flex gap-5"
            >
              <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center flex-shrink-0 shadow-glow-brand/20`}>
                <Icon className="text-white text-2xl" />
              </div>
              <div>
                <h3 className="font-display font-semibold text-white mb-2">{title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 border-t border-dark-600">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="card p-10 border-brand-500/20 bg-gradient-to-b from-brand-500/5 to-transparent"
          >
            <h2 className="font-display font-bold text-3xl text-white mb-4">Ready to accelerate your career?</h2>
            <p className="text-slate-400 mb-8">Join thousands of students and alumni building meaningful connections.</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link to="/register?role=student" className="btn-primary px-8 py-3">I'm a Student</Link>
              <Link to="/register?role=alumni"  className="btn-secondary px-8 py-3">I'm an Alumni</Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-dark-600 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-slate-500 text-sm">
            <RiBrainLine className="text-brand-400" />
            <span className="font-display">AI CareerVerse</span>
            <span>© 2025</span>
          </div>
          <p className="text-xs text-slate-600">Built with Flask · React · SQLAlchemy · SentenceTransformers</p>
        </div>
      </footer>
    </div>
  );
}
