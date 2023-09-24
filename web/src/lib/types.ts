import type { Readable, Writable } from "svelte/store"
import { currentApp, navExpanded, navScrollTop } from "$lib/stores"

export enum EIcon {
    Folder = "Folder",
    Menu = "Menu",
    Proxy = "Proxy",
    RStudio = "RStudio",
    Terminal = "Terminal",
}

export type App = {
    name: string
    href: string
    icon: EIcon
}

export class Store {
    currentApp: Readable<App | undefined>
    navExpanded: Writable<boolean>
    navScrollTop: Writable<number>

    constructor() {
        this.currentApp = currentApp()
        this.navExpanded = navExpanded()
        this.navScrollTop = navScrollTop()
    }
}
