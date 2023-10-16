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

export function asSearchParams(form: HTMLFormElement): URLSearchParams {
    return new URLSearchParams(
        Array.from(new FormData(form), ([key, value]: [string, FormDataEntryValue]) => [key, value as string])
    )
}

export function getFlow(url: string | undefined): string {
    if (typeof url === "undefined") {
        return ""
    }

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
    return `${slug[0].toUpperCase() + slug.slice(1)} | ${SITE_TITLE}`
}
