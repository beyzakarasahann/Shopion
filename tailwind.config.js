/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",  // HTML ve JS dosyalarını dinler
    "./static/**/*.{html,js}",     // Static dosyaları (CSS, JS) dinler
  ],
  theme: {
    extend: {},
  },
  plugins: [
        require('@tailwindcss/line-clamp'),
  ],
}
