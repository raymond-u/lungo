import { derived, type Readable, writable, type Writable } from "svelte/store"
import type { Page } from "@sveltejs/kit"
import { page } from "$app/stores"
import { type AppInfo, ETheme } from "$lib/types"

export function allowScroll(): Writable<boolean> {
    return writable(true)
}

export function currentApp(page: Readable<Page>): Readable<AppInfo | undefined> {
    return derived(page, ($page: Page) =>
        $page.data.apps?.find((app: AppInfo) => $page.url.pathname.startsWith(app.href))
    )
}

export function currentInlineFrame(): Writable<HTMLIFrameElement | undefined> {
    return writable(undefined)
}

export function currentTheme(): Writable<ETheme> {
    return writable(ETheme.Auto)
}

export function darkTheme(currentTheme: Writable<ETheme>): Readable<boolean | undefined> {
    return derived(currentTheme, ($currentTheme: ETheme) => {
        switch ($currentTheme) {
            case ETheme.Auto:
                return typeof matchMedia === "undefined"
                    ? undefined
                    : matchMedia("(prefers-color-scheme: dark)").matches
            case ETheme.Dark:
            case ETheme.Dracula:
            case ETheme.Synthwave:
                return true
            default:
                return false
        }
    })
}

export function loginForm(): Writable<object | undefined> {
    return writable(undefined)
}

export function syncedScrollTop(): Writable<number> {
    return writable(0)
}

export class Store {
    allowScroll: Writable<boolean>
    currentApp: Readable<AppInfo | undefined>
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
