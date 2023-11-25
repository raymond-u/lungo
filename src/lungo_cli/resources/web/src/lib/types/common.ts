import type { Readable, Writable } from "svelte/store"
import { page } from "$app/stores"
import { allowScroll, currentApp, currentInlineFrame, currentTheme, darkTheme, loginForm } from "$lib/stores"

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

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<App | undefined>
    currentInlineFrame: Writable<HTMLIFrameElement | undefined>
    currentTheme: Writable<ETheme>
    darkTheme: Readable<boolean | undefined>
    loginForm: Writable<object | undefined>
    syncedScrollTops: { [key: string]: Writable<number> }

    constructor() {
        this.allowScroll = allowScroll()
        this.currentApp = currentApp(page)
        this.currentInlineFrame = currentInlineFrame()
        this.currentTheme = currentTheme()
        this.darkTheme = darkTheme(this.currentTheme)
        this.loginForm = loginForm()
        this.syncedScrollTops = {}
    }
}
