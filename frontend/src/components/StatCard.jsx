/**
 * components/StatCard.jsx — Animated metric card
 */
import { motion } from "framer-motion";
import clsx from "clsx";

export default function StatCard({ icon: Icon, label, value, sub, color = "brand", delay = 0, trend }) {
  const colorMap = {
    brand:  { bg: "bg-brand-500/10",        text: "text-brand-300",        border: "border-brand-500/20" },
    green:  { bg: "bg-accent-green/10",     text: "text-emerald-300",      border: "border-accent-green/20" },
    violet: { bg: "bg-accent-violet/10",    text: "text-violet-300",       border: "border-accent-violet/20" },
    amber:  { bg: "bg-accent-amber/10",     text: "text-amber-300",        border: "border-accent-amber/20" },
    rose:   { bg: "bg-accent-rose/10",      text: "text-rose-300",         border: "border-accent-rose/20" },
    cyan:   { bg: "bg-accent-cyan/10",      text: "text-cyan-300",         border: "border-accent-cyan/20" },
  };
  const c = colorMap[color] || colorMap.brand;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: "easeOut" }}
      className={clsx("stat-card border", c.border, "hover:shadow-card-dark hover:-translate-y-0.5 transition-all duration-200")}
    >
      <div className="flex items-start justify-between">
        <div className={clsx("w-10 h-10 rounded-xl flex items-center justify-center", c.bg)}>
          <Icon className={clsx("text-xl", c.text)} />
        </div>
        {trend !== undefined && (
          <span className={clsx("text-xs font-display font-medium px-2 py-0.5 rounded-full",
            trend >= 0 ? "bg-accent-green/10 text-emerald-300" : "bg-accent-rose/10 text-rose-300"
          )}>
            {trend >= 0 ? "↑" : "↓"} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <div>
        <p className="text-2xl font-display font-bold text-white">{value}</p>
        <p className="text-xs font-display text-slate-400 uppercase tracking-wider">{label}</p>
        {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
      </div>
    </motion.div>
  );
}
