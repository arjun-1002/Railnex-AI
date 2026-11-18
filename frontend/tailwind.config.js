/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        railway: {
          navy: '#0f172a',
          slate: '#1e293b',
          blue: '#2563eb',
          darkblue: '#1d4ed8',
          lightblue: '#dbeafe',
          alert: '#ef4444',
          warning: '#f59e0b',
          success: '#10b981'
        }
      }
    },
  },
  plugins: [],
}
