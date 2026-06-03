/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // AI CareerVerse brand palette
        brand: {
          50:  "#f0f4ff",
          100: "#e0e9ff",
          200: "#c0d2ff",
          300: "#90aeff",
          400: "#5a7fff",
          500: "#3355ff",
          600: "#1c35e8",
          700: "#1628cc",
          800: "#1824a6",
          900: "#192184",
        },
        accent: {
          cyan:   "#06d6d6",
          violet: "#7c3aed",
          rose:   "#f43f5e",
          amber:  "#f59e0b",
          green:  "#10b981",
        },
        dark: {
          900: "#030407",
          800: "#080c14",
          700: "#0d1526",
          600: "#111d35",
          500: "#172040",
          400: "#1e2850",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body:    ["'DM Sans'", "sans-serif"],
        mono:    ["'JetBrains Mono'", "monospace"],
      },
      backgroundImage: {
        "grid-pattern": "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%233355ff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
        "hero-gradient": "radial-gradient(ellipse 80% 60% at 50% -10%, rgba(51,85,255,0.3) 0%, transparent 60%), radial-gradient(ellipse 40% 30% at 80% 80%, rgba(124,58,237,0.2) 0%, transparent 50%)",
      },
      boxShadow: {
        "glow-brand": "0 0 30px rgba(51,85,255,0.4)",
        "glow-cyan":  "0 0 20px rgba(6,214,214,0.3)",
        "card-dark":  "0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.05) inset",
      },
      animation: {
        "fade-up":    "fadeUp 0.5s ease forwards",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "shimmer":    "shimmer 2s linear infinite",
        "float":      "float 6s ease-in-out infinite",
      },
      keyframes: {
        fadeUp: {
          "0%":   { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%":      { transform: "translateY(-10px)" },
        },
      },
    },
  },
  plugins: [],
};
