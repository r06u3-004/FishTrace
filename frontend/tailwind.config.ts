import type { Config } from "tailwindcss"

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "var(--ft-bg)",
        surface: "var(--ft-surface)",
        elevated: "var(--ft-surface-2)",
        accent: "var(--ft-accent)",
        ink: "var(--ft-text)",
        muted: "var(--ft-text-muted)",
        line: "var(--ft-border)",
        critical: "var(--ft-critical)",
        high: "var(--ft-high)",
        medium: "var(--ft-medium)",
        low: "var(--ft-low)",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      borderRadius: {
        DEFAULT: "4px",
        md: "6px",
        lg: "8px",
      },
    },
  },
  plugins: [],
} satisfies Config
