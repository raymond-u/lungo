import type { ComponentType } from "svelte"

export type AppInfo = {
    name: string
    descriptiveName: string
    href: string
    icon: ComponentType
    altIcon: ComponentType
}

export type RawAppInfo = {
    name: string
    descriptiveName: string | null
    icon: string | null
    altIcon: string | null
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
