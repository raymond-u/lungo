const daisyui = require("daisyui")

/** @type {import("tailwindcss").Config}*/
const config = {
    content: ["./src/**/*.{html,js,svelte,ts}"],

    daisyui: {
        logs: false,
        themes: [
            {
                light: {
                    "color-scheme": "light",
                    "primary": "#570df8",
                    "primary-content": "#E0D2FE",
                    "secondary": "#f000b8",
                    "secondary-content": "#FFD1F4",
                    "accent": "#1ECEBC",
                    "accent-content": "#07312D",
                    "neutral": "#2B3440",
                    "neutral-content": "#D7DDE4",
                    "base-100": "#ffffff",
                    "base-200": "#F2F2F2",
                    "base-300": "#E5E6E6",
                    "base-content": "#1f2937",
                },
                dark: {
                    "color-scheme": "dark",
                    "primary": "#661AE6",
                    "primary-content": "#ffffff",
                    "secondary": "#D926AA",
                    "secondary-content": "#ffffff",
                    "accent": "#1FB2A5",
                    "accent-content": "#ffffff",
                    "neutral": "#2a323c",
                    "neutral-focus": "#242b33",
                    "neutral-content": "#A6ADBB",
                    "base-100": "#1d232a",
                    "base-200": "#191e24",
                    "base-300": "#15191e",
                    "base-content": "#A6ADBB",
                }
            },
        ],
    },

    theme: {
        extend: {},
    },

    plugins: [daisyui],
}

module.exports = config
