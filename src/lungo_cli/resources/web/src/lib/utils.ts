import { getContext, setContext } from "svelte"
import { SITE_TITLE } from "$lib/constants"
import { Store } from "$lib/types"

export function createStore(): Store {
    const store = new Store()
    setContext("globalStore", store)

    return store
}

export function useStore(): Store {
    return getContext<Store>("globalStore")
}

export function isSameHost(url: string | URL, host: string): boolean {
    if (typeof url === "string" && !url.match("^(?:https?|wss?)://")) {
        return true
    }

    return new URL(url).host === host
}

export function getFlow(url: string): string {
    return new URL(url).searchParams.get("flow") ?? ""
}

export function getPlaceholder(firstName: string, lastName: string): string {
    return `${firstName[0].toUpperCase()}${lastName[0].toUpperCase()}`
}

export function getRandomElement<T>(array: T[]): T {
    return array[Math.floor(Math.random() * array.length)]
}

export function getRandomId(): number {
    return Number(Math.round(Math.random() * 100000).toString() + Date.now().toString().slice(-5))
}

export function getTitleFromSlug(slug: string): string {
    return `${slug[0]?.toUpperCase() ?? ""}${slug.slice(1)} | ${SITE_TITLE}`
}

export function getTruncateTitle(title: string, length: number): string {
    if (title.length > length) {
        const capitalSplit = title[0] + title.slice(1).split(/[A-Z]/)[0]
        const spaceSplit = title.split(" ")[0]

        return capitalSplit.length < spaceSplit.length ? capitalSplit : spaceSplit
    } else {
        return title
    }
}

export function getUrlParts(url: string): { path: string; query: string; hash: string } {
    const [path, other] = url.split("?", 2)

    if (other) {
        const [query, hash] = other.split("#", 2)

        return {
            path,
            query: `?${query}`,
            hash: hash ? `#${hash}` : "",
        }
    }

    return {
        path,
        query: "",
        hash: "",
    }
}
