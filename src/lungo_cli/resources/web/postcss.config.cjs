const nesting = require("tailwindcss/nesting")
const tailwindcss = require("tailwindcss")
const autoprefixer = require("autoprefixer")

const config = {
    plugins: [
        nesting,
        tailwindcss(),
        autoprefixer,
    ],
}

module.exports = config
