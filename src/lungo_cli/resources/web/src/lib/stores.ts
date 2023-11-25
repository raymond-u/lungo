import { derived, type Readable, writable, type Writable } from "svelte/store"
import type { Page } from "@sveltejs/kit"
import { type App, ETheme } from "$lib/types"

export function allowScroll(): Writable<boolean> {
    return writable(true)
}

export function currentApp(page: Readable<Page>): Readable<App | undefined> {
    return derived(page, ($page: Page) => $page.data.apps?.find((app: App) => $page.url.pathname.startsWith(app.href)))
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
