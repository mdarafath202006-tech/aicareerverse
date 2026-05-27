/**
 * api/client.js — Axios instance with JWT interceptors
 */
import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token automatically
api.interceptors.request.use((config) => {
  try {
    const state = JSON.parse(localStorage.getItem("aicareerverse") || "{}");
    const token = state?.state?.token;
    if (token) config.headers.Authorization = `Bearer ${token}`;
  } catch (_) {}
  return config;
});

// Handle 401 globally
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("aicareerverse");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Typed API functions ───────────────────────────────────────────────────
export const authApi = {
  login:    (email, password) => api.post("/auth/login", { email, password }),
};

export const alumniApi = {
  getAll:          ()     => api.get("/recommendations"),
  getById:         (id)   => api.get(`/alumni/${id}`),
  getAnalytics:    ()     => api.get("/analytics"),
};

export const skillApi = {
  getGap: (targetRole) => api.post("/skill-gap", { target_role: targetRole }),
};
