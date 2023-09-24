import { derived, writable, type Readable, type Writable } from "svelte/store"
import { page } from "$app/stores"
import type { App } from "$lib/types"
import type { Page } from "@sveltejs/kit"

export function allowScroll(): Writable<boolean> {
    return writable(true)
}

export function currentApp(): Readable<App | undefined> {
    return derived(
        page,
        ($page: Page) => $page.data.apps?.find((app: App): boolean => $page.url.pathname.startsWith(app.href))
    )
}

export function syncedScrollTop(): Writable<number> {
    return writable(0)
}
