module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF6B6B',       // Color primario
        secondary: '#4ECDC4',     // Color secundario
        background: '#F7F7F7',    // Color de fondo
        text: '#333333',          // Color de texto principal
        lightText: '#777777',     // Color de texto secundario
      },
      fontFamily: {
        nunito: ['Nunito', 'sans-serif'], // Fuente personalizada
      },
      boxShadow: {
        custom: '0 0.5rem 1rem rgba(0, 0, 0, 0.08)', // Sombra personalizada
      },
    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
};