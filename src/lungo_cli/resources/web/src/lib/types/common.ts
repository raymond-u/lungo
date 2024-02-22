export type App = {
    name: string
    href: string
    icon: EIcon
}

export enum EIcon {
    Folder,
    Jupyter,
    Menu,
    Note,
    Proxy,
    RStudio,
    Terminal,
    Theme,
    Visibility,
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
