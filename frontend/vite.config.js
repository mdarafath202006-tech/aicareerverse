import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api":      { target: "http://localhost:5000", changeOrigin: true },
      "/student":  { target: "http://localhost:5000", changeOrigin: true },
      "/alumni":   { target: "http://localhost:5000", changeOrigin: true },
      "/analytics":{ target: "http://localhost:5000", changeOrigin: true },
      "/login":    { target: "http://localhost:5000", changeOrigin: true },
      "/register": { target: "http://localhost:5000", changeOrigin: true },
      "/socket.io":{ target: "http://localhost:5000", ws: true, changeOrigin: true },
    },
  },
  build: {
    outDir: "../app/static/react",
    emptyOutDir: true,
  },
});
