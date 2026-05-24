/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#08111f",
        ocean: "#0f766e",
        sunrise: "#f97316",
        mint: "#d1fae5",
        panel: "#0f172a"
      },
      boxShadow: {
        glow: "0 20px 60px rgba(15, 118, 110, 0.18)"
      }
    }
  },
  plugins: []
};
