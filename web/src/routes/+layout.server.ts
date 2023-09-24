import { EIcon } from "$lib/types"

// noinspection JSUnusedGlobalSymbols
export function load() {
    return {
        apps: [
            { name: "Terminal", href: "/app/terminal", icon: EIcon.Terminal },
            { name: "Proxy", href: "/app/proxy", icon: EIcon.Proxy },
            { name: "Files", href: "/app/files", icon: EIcon.Folder },
            { name: "R Studio", href: "/app/r-studio", icon: EIcon.RStudio },
        ],
    }
}
