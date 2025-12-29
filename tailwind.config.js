/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0a0e27',
          card: '#141b2d',
          border: '#1e293b',
          hover: '#1f2937',
        },
        threat: {
          critical: '#ef4444',
          high: '#f59e0b',
          medium: '#eab308',
          low: '#10b981',
          info: '#3b82f6',
        },
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
