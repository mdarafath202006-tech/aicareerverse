/**
 * components/MentorCard.jsx — Animated alumni/mentor card
 */
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { RiBriefcaseLine, RiMapPinLine, RiLinkedinBoxLine, RiSparklingLine } from "react-icons/ri";
import clsx from "clsx";

export default function MentorCard({ alumni, percent, matchedSkills = [], delay = 0, onRequest }) {
  const initials = alumni?.name
    ? alumni.name.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase()
    : "??";

  const scoreColor =
    percent >= 70 ? "text-emerald-300" :
    percent >= 40 ? "text-amber-300" : "text-rose-300";

  const scoreBg =
    percent >= 70 ? "bg-accent-green/10 border-accent-green/20" :
    percent >= 40 ? "bg-accent-amber/10 border-accent-amber/20" : "bg-accent-rose/10 border-accent-rose/20";

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: "easeOut" }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="card-hover p-5 group flex flex-col gap-4"
    >
      {/* Header */}
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center text-white font-display font-bold text-lg flex-shrink-0 shadow-glow-brand/30">
          {initials}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-display font-semibold text-white text-sm truncate">{alumni?.name}</h3>
          <div className="flex items-center gap-1.5 mt-0.5">
            <RiBriefcaseLine className="text-brand-300 text-xs flex-shrink-0" />
            <p className="text-xs text-slate-400 truncate">{alumni?.job_role || "Professional"}</p>
          </div>
          {alumni?.company && (
            <p className="text-xs text-slate-500 mt-0.5">@ {alumni.company}</p>
          )}
        </div>
        {/* Match score */}
        {percent > 0 && (
          <div className={clsx("flex-shrink-0 border rounded-xl px-3 py-1.5 text-center", scoreBg)}>
            <RiSparklingLine className={clsx("text-xs mx-auto mb-0.5", scoreColor)} />
            <p className={clsx("text-sm font-display font-bold leading-none", scoreColor)}>{percent}%</p>
            <p className="text-[9px] text-slate-500">match</p>
          </div>
        )}
      </div>

      {/* Location */}
      {alumni?.location && (
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <RiMapPinLine />
          <span>{alumni.location}</span>
        </div>
      )}

      {/* Matched skills */}
      {matchedSkills.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {matchedSkills.slice(0, 4).map(skill => (
            <span key={skill} className="badge-brand text-[10px]">{skill}</span>
          ))}
          {matchedSkills.length > 4 && (
            <span className="badge-brand text-[10px]">+{matchedSkills.length - 4}</span>
          )}
        </div>
      )}

      {/* Progress bar */}
      {percent > 0 && (
        <div>
          <div className="progress-bar">
            <motion.div
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{ width: `${percent}%` }}
              transition={{ duration: 0.8, delay: delay + 0.3, ease: "easeOut" }}
            />
          </div>
          <p className="text-[10px] text-slate-600 mt-1">{percent}% compatibility</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2 mt-auto pt-1">
        {alumni?.linkedin && (
          <a
            href={alumni.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-ghost btn-sm"
          >
            <RiLinkedinBoxLine className="text-blue-400" />
            <span className="text-xs">LinkedIn</span>
          </a>
        )}
        <button
          onClick={() => onRequest?.(alumni)}
          className="btn-primary btn-sm flex-1 justify-center"
        >
          Request Mentor
        </button>
      </div>
    </motion.div>
  );
}
