/**
 * store/useStore.js — Global Zustand state store
 * Manages: auth, notifications, theme, sidebar, socket
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import axios from "axios";

const useStore = create(
  persist(
    (set, get) => ({
      // ── Auth ──────────────────────────────────────────────────────────
      user:       null,
      token:      null,
      isLoggedIn: false,

      setUser: (user, token) => set({ user, token, isLoggedIn: !!user }),
      logout: () => {
        set({ user: null, token: null, isLoggedIn: false });
        axios.get("/logout");
      },

      // ── Notifications ─────────────────────────────────────────────────
      notifications:       [],
      unreadCount:         0,
      notificationsLoaded: false,

      fetchNotifications: async () => {
        try {
          const { data } = await axios.get("/api/notifications");
          set({
            notifications:       data,
            unreadCount:         data.filter(n => !n.is_read).length,
            notificationsLoaded: true,
          });
        } catch (_) {}
      },

      markRead: async (id) => {
        await axios.post(`/api/notifications/${id}/read`);
        set(s => ({
          notifications: s.notifications.map(n => n.id === id ? { ...n, is_read: true } : n),
          unreadCount:   Math.max(0, s.unreadCount - 1),
        }));
      },

      addNotification: (notif) =>
        set(s => ({
          notifications: [notif, ...s.notifications],
          unreadCount:   s.unreadCount + 1,
        })),

      // ── UI ────────────────────────────────────────────────────────────
      sidebarOpen: true,
      darkMode:    true,

      toggleSidebar: () => set(s => ({ sidebarOpen: !s.sidebarOpen })),
      toggleDark:    () => set(s => ({ darkMode: !s.darkMode })),

      // ── Online users ──────────────────────────────────────────────────
      onlineCount: 0,
      setOnlineCount: (count) => set({ onlineCount: count }),
    }),
    {
      name:    "aicareerverse",
      partialize: (s) => ({ user: s.user, token: s.token, isLoggedIn: s.isLoggedIn, darkMode: s.darkMode }),
    }
  )
);

export default useStore;
