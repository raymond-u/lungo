import { getContext, setContext } from "svelte"
import { SITE_TITLE } from "$lib/constants"
import { Store } from "$lib/stores"
import { capitalize } from "$lib/utils"

export function createStore(): Store {
    const store = new Store()
    setContext("globalStore", store)

    return store
}

export function getPageTitle(slug: string): string {
    return `${capitalize(slug)} | ${SITE_TITLE}`
}

export function useStore(): Store {
    return getContext<Store>("globalStore")
}
