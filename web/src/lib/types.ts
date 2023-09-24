import type { Readable, Writable } from "svelte/store"
import { currentApp, allowScroll } from "$lib/stores"

export type App = {
    name: string
    href: string
    icon: EIcon
}

export enum EIcon {
    Folder = "Folder",
    Menu = "Menu",
    Proxy = "Proxy",
    RStudio = "RStudio",
    Terminal = "Terminal",
}

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<App | undefined>
    syncedScrollTops: { [key: string]: Writable<number> }

    constructor() {
        this.allowScroll = allowScroll()
        this.currentApp = currentApp()
        this.syncedScrollTops = {}
    }
}
