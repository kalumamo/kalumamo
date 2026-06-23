import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

/**
 * All requests go through the Next.js rewrite proxy at /api/* which forwards
 * to http://localhost:8000/api/* (or http://backend:8000/api/* in Docker).
 *
 * This avoids CORS entirely — the browser only talks to the same origin.
 * Never hardcode http://localhost:8000 here — it breaks in Docker and
 * causes CORS preflight failures in production.
 */
const api = axios.create({
  baseURL: "/api",          // relative — uses Next.js rewrite proxy
  headers: { "Content-Type": "application/json" },
  timeout: 120000,           // 2 min — model training can take time
});

// ── Attach JWT access token & handle FormData ────────────────────────────
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Don't set Content-Type for FormData — let axios/browser handle it
  if (config.data instanceof FormData) {
    delete config.headers["Content-Type"];
  }
  
  return config;
});

// ── Auto-refresh token on 401 ────────────────────────────────────────────
api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          // Use the same relative proxy path
          const { data } = await axios.post("/api/auth/refresh", {
            refresh_token: refreshToken,
          });
          localStorage.setItem("access_token", data.access_token);
          original.headers.Authorization = `Bearer ${data.access_token}`;
          return api(original);
        }
      } catch {
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
