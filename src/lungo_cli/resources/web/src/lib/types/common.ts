import type { Readable, Writable } from "svelte/store"
import { allowScroll, currentApp, currentInlineFrame, darkTheme, loginForm } from "$lib/stores"

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

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<App | undefined>
    currentInlineFrame: Writable<HTMLIFrameElement | undefined>
    darkTheme: Writable<boolean | undefined>
    loginForm: Writable<object | undefined>
    syncedScrollTops: { [key: string]: Writable<number> }

    constructor() {
        this.allowScroll = allowScroll()
        this.currentApp = currentApp()
        this.currentInlineFrame = currentInlineFrame()
        this.darkTheme = darkTheme()
        this.loginForm = loginForm()
        this.syncedScrollTops = {}
    }
}
