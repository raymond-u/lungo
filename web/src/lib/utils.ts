import { getContext, setContext } from "svelte"
import { SITE_TITLE } from "$lib/constants"
import { Store } from "$lib/types"

export function asSearchParams(form: HTMLFormElement): URLSearchParams {
    return new URLSearchParams(
        Array.from(new FormData(form), ([key, value]: [string, FormDataEntryValue]) => [key, value as string])
    )
}

export function formatTitle(title: string): string {
    return `${title} | ${SITE_TITLE}`
}

export function createStore(): Store {
    const store = new Store()
    setContext("globalStore", store)

    return store
}

export function useStore(): Store {
    return getContext<Store>("globalStore")
}
