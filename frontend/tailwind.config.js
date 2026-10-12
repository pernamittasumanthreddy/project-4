/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#123B52',
        'primary-hover': '#0B2C3D',
        secondary: '#0F8B8D',
        'secondary-hover': '#0B7476',
        medNavy: '#123B52',
        medTeal: '#0F8B8D',
        medBg: '#F4F7FA',
        medBorder: '#DCE4EA',
        gateway: {
          lightBg: '#F4F7FA',
          lightSurface: '#FFFFFF',
          lightBorder: '#DCE4EA',
          lightText: '#1E293B',
          lightMuted: '#64748B',
          
          darkBg: '#0B1120',
          darkBgAlt: '#111827',
          darkSurface: '#172033',
          darkElevated: '#1D293D',
          darkBorder: '#293548',
          darkText: '#F8FAFC',
          darkMuted: '#A8B4C7',
          
          primary: '#123B52',
          primaryHover: '#0B2C3D',
          primaryDark: '#60A5FA',
          primaryDarkHover: '#93C5FD',
          
          teal: '#0F8B8D',
          tealDark: '#0B7476',
          
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
