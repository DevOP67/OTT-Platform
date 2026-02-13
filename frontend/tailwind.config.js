/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: '#050505',
          paper: '#0A0A0A',
          subtle: '#121212',
        },
        primary: {
          DEFAULT: '#00E5FF',
          hover: '#00B8CC',
        },
        secondary: {
          DEFAULT: '#FF3B30',
          hover: '#D63025',
        },
        text: {
          primary: '#EDEDED',
          secondary: '#A1A1AA',
          muted: '#52525B',
        },
        border: {
          DEFAULT: 'rgba(255, 255, 255, 0.1)',
          active: 'rgba(0, 229, 255, 0.3)',
        },
      },
      fontFamily: {
        heading: ['Manrope', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        glow: '0 0 20px rgba(0, 229, 255, 0.2)',
        card: '0 10px 30px -10px rgba(0, 0, 0, 0.5)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
