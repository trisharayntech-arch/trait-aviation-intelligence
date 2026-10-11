/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aviation: {
          dark: '#0B132B',
          navy: '#1C2541',
          slate: '#3A506B',
          cyan: '#00F0FF',
          teal: '#5BC0BE',
          accent: '#6FFFE9',
          amber: '#F59E0B',
          rose: '#EF4444',
          emerald: '#10B981',
          card: '#131F38',
          cardBorder: '#22355A'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      }
    },
  },
  plugins: [],
}
