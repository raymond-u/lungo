import type { Readable, Writable } from "svelte/store"
import { allowScroll, currentApp, darkTheme, loginForm } from "$lib/stores"

export type App = {
    name: string
    href: string
    icon: EIcon
}

export enum EDependency {
    Form = "form",
    Session = "session",
}

export enum EIcon {
    Folder,
    Menu,
    Proxy,
    RStudio,
    Terminal,
    Theme,
    Visibility,
}

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<App | undefined>
    darkTheme: Writable<boolean | undefined>
    loginForm: Writable<object | undefined>
    syncedScrollTops: { [key: string]: Writable<number> }

    constructor() {
        this.allowScroll = allowScroll()
        this.currentApp = currentApp()
        this.darkTheme = darkTheme()
        this.loginForm = loginForm()
        this.syncedScrollTops = {}
    }
}