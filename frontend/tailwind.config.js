/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gateway: {
          lightBg: '#F5F8FC',
          lightSurface: '#FFFFFF',
          lightBorder: '#DCE4EF',
          lightText: '#0F172A',
          lightMuted: '#64748B',
          
          darkBg: '#0B1120',
          darkBgAlt: '#111827',
          darkSurface: '#172033',
          darkElevated: '#1D293D',
          darkBorder: '#293548',
          darkText: '#F8FAFC',
          darkMuted: '#A8B4C7',
          
          primary: '#2563EB',
          primaryHover: '#1D4ED8',
          primaryDark: '#60A5FA',
          primaryDarkHover: '#93C5FD',
          
          teal: '#0F9D8A',
          tealDark: '#2DD4BF',
          
          success: '#16A34A',
          successDark: '#4ADE80',
          
          warning: '#D97706',
          warningDark: '#FBBF24',
          
          danger: '#DC2626',
          dangerDark: '#F87171',
        },
        hospital: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#bae0fd',
          300: '#7cc7fb',
          400: '#38a8f6',
          500: '#0e8ce8',
          600: '#026fc6',
          700: '#0358a0',
          800: '#074b83',
          900: '#0c3f6d',
          950: '#072848',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
};
