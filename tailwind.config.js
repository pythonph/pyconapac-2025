/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.html"],
  theme: {
    extend: {
      screens: {
        xs: "320px",
        // => @media (min-width: 320px) { ... }
      },
    },
  },
  plugins: [
    function ({ addComponents }) {
      addComponents({
        ".container": {
          maxWidth: "100%",
          "@screen sm": {
            maxWidth: "640px",
          },
          "@screen md": {
            maxWidth: "768px",
          },
          "@screen lg": {
            maxWidth: "990px",
          },
          "@screen xl": {
            maxWidth: "990px",
          },
        },
      });
    },
  ],
};
