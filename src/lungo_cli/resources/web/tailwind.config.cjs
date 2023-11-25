const typography = require("@tailwindcss/typography")
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
                    "primary": "#570DF8",
                    "primary-content": "#F6F6F6",
                    "secondary": "#F000B8",
                    "secondary-content": "#F6F6F6",
                    "accent": "#1ECEBC",
                    "accent-content": "#07312D",
                    "neutral": "#2B3440",
                    "neutral-content": "#D7DDE4",
                    "base-100": "#F5F5F5",
                    "base-200": "#EBEBEB",
                    "base-300": "#E0E0E0",
                    "base-content": "#1F2937",
                },
                dark: {
                    "color-scheme": "dark",
                    "primary": "#661AE6",
                    "primary-content": "#FFFFFF",
                    "secondary": "#D926AA",
                    "secondary-content": "#FFFFFF",
                    "accent": "#1FB2A5",
                    "accent-content": "#FFFFFF",
                    "neutral": "#2A323C",
                    "neutral-focus": "#242B33",
                    "neutral-content": "#A6ADBB",
                    "base-100": "#1D232A",
                    "base-200": "#191E24",
                    "base-300": "#15191E",
                    "base-content": "#A6ADBB",
                }
            },
            "emerald",
            "synthwave",
            "lofi",
            "dracula",
        ],
    },

    theme: {
        extend: {},
    },

    plugins: [
        typography,
        daisyui,
    ],
}

module.exports = config
