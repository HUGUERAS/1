/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          primary: '#4F46E5',
          secondary: '#7C3AED',
        },
        success: '#16A34A',
        info: '#2563EB',
      },
    },
  },
  plugins: [],
}

