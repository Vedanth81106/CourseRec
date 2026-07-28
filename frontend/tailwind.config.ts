import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#d9e6ff",
          200: "#b3ccff",
          300: "#82a9ff",
          400: "#4f7fff",
          500: "#2657f5",
          600: "#1b40d1",
          700: "#1731a3",
          800: "#152a80",
          900: "#152667",
        },
      },
    },
  },
  plugins: [],
};

export default config;
