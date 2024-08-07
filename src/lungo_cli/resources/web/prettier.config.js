export default {
    useTabs: false,
    semi: false,
    singleQuote: false,
    trailingComma: "es5",
    printWidth: 120,
    htmlWhitespaceSensitivity: "ignore",
    plugins: ["prettier-plugin-svelte", "prettier-plugin-tailwindcss"],
    overrides: [
        {
            files: "*.svelte",
            options: {
                parser: "svelte",
            },
        },
    ],
}
