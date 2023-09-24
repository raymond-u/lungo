import type { ActionReturn } from "svelte/action"
import type { Writable } from "svelte/store"
import { syncedScrollTop } from "$lib/stores"

type SSAttrs = { class: `${string}overflow${"-y" | ""}-auto${string}` }
type SSParams = { stores: { [key: string]: Writable<number> }; id: string }

export function syncScroll(node: HTMLElement, { stores, id }: SSParams): ActionReturn<SSParams, SSAttrs> {
    if (!(id in stores)) {
        stores[id] = syncedScrollTop()
    }

    const handleFocus = () => {
        stores[id].set(node.scrollTop)
    }

    const unsubscribe = stores[id].subscribe((scrollTop: number) => {
        if (node.scrollTop !== scrollTop) {
            node.scrollTop = scrollTop
        }
    })

    node.addEventListener("scroll", handleFocus)

    return {
        destroy() {
            node.removeEventListener("scroll", handleFocus)
            unsubscribe()
        },
    }
}
