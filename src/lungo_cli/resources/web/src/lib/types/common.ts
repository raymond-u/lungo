import type { ComponentType } from "svelte"

export type AppInfo = {
    name: string
    descriptiveName: string
    href: string
    icon: ComponentType
    altIcon: ComponentType
}

// noinspection JSUnusedGlobalSymbols
export enum ETheme {
    Auto = "auto",
    Light = "light",
    Dark = "dark",
    Emerald = "emerald",
    Synthwave = "synthwave",
    LoFi = "lofi",
    Dracula = "dracula",
}
