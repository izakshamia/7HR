/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './client/pages/**/*.{ts,tsx}',
    './client/components/**/*.{ts,tsx}',
    './client/app/**/*.{ts,tsx}',
    './client/src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "rgba(255, 255, 255, 0.1)",
        input: "rgba(255, 255, 255, 0.1)",
        ring: "rgba(255, 215, 0, 0.6)",
        background: "#0a0f1f",
        foreground: "#ffffff",
        primary: {
          DEFAULT: "#ffd700",
          foreground: "#1a2036",
        },
        secondary: {
          DEFAULT: "#b0b8c5",
          foreground: "#1a2036",
        },
        destructive: {
          DEFAULT: "#b8860b",
          foreground: "#1a2036",
        },
        muted: {
          DEFAULT: "rgba(255, 215, 0, 0.08)",
          foreground: "#b0b8c5",
        },
        accent: {
          DEFAULT: "rgba(255, 215, 0, 0.08)",
          foreground: "#ffd700",
        },
        popover: {
          DEFAULT: "rgba(26, 32, 54, 0.6)",
          foreground: "#ffffff",
        },
        card: {
          DEFAULT: "rgba(26, 32, 54, 0.6)",
          foreground: "#ffffff",
          border: "rgba(255, 215, 0, 0.15)",
        },
        gold: {
          DEFAULT: "#ffd700",
          darker: "#e6c200",
          bronze: "#b8860b",
          brighter: "#fff176",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
