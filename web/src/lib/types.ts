import type { Readable, Writable } from "svelte/store"
import { allowScroll, currentApp, loginForm } from "$lib/stores"

export type App = {
    name: string
    href: string
    icon: EIcon
}

export type Fetch = ((input: RequestInfo | URL, init?: RequestInit | undefined) => Promise<Response>) | undefined

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
    Visibility,
}

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<App | undefined>
    loginForm: Writable<object | undefined>
    syncedScrollTops: { [key: string]: Writable<number> }

    constructor() {
        this.allowScroll = allowScroll()
        this.currentApp = currentApp()
        this.loginForm = loginForm()
        this.syncedScrollTops = {}
    }
}
