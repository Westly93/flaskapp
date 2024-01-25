/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./flaskapp/templates/**/*.html",
      "./flaskapp/static/src/**/*.js",
      "./node_modules/flowbite/**/*.js"
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require("flowbite/plugin")
  ]
  }
  
  