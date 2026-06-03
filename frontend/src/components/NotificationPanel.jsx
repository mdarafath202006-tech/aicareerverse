/**
 * components/NotificationPanel.jsx
 */
import { motion } from "framer-motion";
import { useEffect, useRef } from "react";
import { RiBellLine, RiCheckLine, RiCloseLine } from "react-icons/ri";
import useStore from "../store/useStore";
import { formatDistanceToNow } from "date-fns";
import clsx from "clsx";

const typeColors = {
  mentor_accepted: "text-accent-green",
  mentor_request:  "text-brand-300",
  placement_alert: "text-accent-amber",
  default:         "text-slate-400",
};

const typeIcons = {
  mentor_accepted: "🎉",
  mentor_request:  "👋",
  placement_alert: "🚀",
  default:         "🔔",
};

export default function NotificationPanel({ onClose }) {
  const { notifications, markRead, fetchNotifications } = useStore();
  const ref = useRef();

  useEffect(() => {
    fetchNotifications();
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) onClose();
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: -8, scale: 0.97 }}
      animate={{ opacity: 1, y: 0,  scale: 1 }}
      exit={{ opacity: 0, y: -8, scale: 0.97 }}
      transition={{ duration: 0.15 }}
      className="absolute right-0 top-12 w-80 z-50 card shadow-card-dark border-dark-500"
    >
      <div className="flex items-center justify-between p-4 border-b border-dark-600">
        <div className="flex items-center gap-2">
          <RiBellLine className="text-brand-300" />
          <span className="font-display font-semibold text-sm text-white">Notifications</span>
        </div>
        <button onClick={onClose} className="text-slate-500 hover:text-white">
          <RiCloseLine />
        </button>
      </div>

      <div className="max-h-80 overflow-y-auto divide-y divide-dark-600">
        {notifications.length === 0 ? (
          <div className="p-6 text-center text-slate-500 text-sm">No notifications yet</div>
        ) : notifications.map((n) => (
          <div
            key={n.id}
            className={clsx("p-4 hover:bg-dark-600/50 transition-colors", !n.is_read && "bg-brand-500/5")}
          >
            <div className="flex gap-3">
              <span className="text-lg flex-shrink-0">{typeIcons[n.type] || typeIcons.default}</span>
              <div className="flex-1 min-w-0">
                <p className={clsx("text-xs font-display font-semibold", typeColors[n.type] || typeColors.default)}>
                  {n.title}
                </p>
                <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{n.message}</p>
                <p className="text-[10px] text-slate-600 mt-1">
                  {n.created_at ? formatDistanceToNow(new Date(n.created_at), { addSuffix: true }) : ""}
                </p>
              </div>
              {!n.is_read && (
                <button
                  onClick={() => markRead(n.id)}
                  className="flex-shrink-0 p-1 rounded-full hover:bg-dark-500 text-slate-500 hover:text-accent-green transition-colors"
                >
                  <RiCheckLine className="text-sm" />
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
