import type { ActionReturn } from "svelte/action"
import type { Writable } from "svelte/store"
import { syncedScrollTop } from "$lib/stores"

type SCParams = { callback: ((e: Event) => void) | ((e: Event) => Promise<void>) }

export function safeClick(node: HTMLButtonElement, { callback }: SCParams): ActionReturn<SCParams> {
    const handleClick = async (e: Event) => {
        if (node.disabled) {
            return
        }

        node.disabled = true

        try {
            await callback(e)
        } finally {
            node.disabled = false
        }
    }

    node.addEventListener("click", handleClick)

    return {
        destroy() {
            node.removeEventListener("click", handleClick)
        },
    }
}

type SSAttrs = { class: `${string}overflow${"-y" | ""}-auto${string}` }

export function scrollShadow(node: HTMLElement): ActionReturn<undefined, SSAttrs> {
    const parent = node.parentNode!
    const container = document.createElement("div")
    const shadow = document.createElement("div")

    container.classList.add("relative", "flex", "flex-1")
    shadow.classList.add(
        "pointer-events-none",
        "absolute",
        "z-10",
        "hidden",
        "h-6",
        "w-full",
        "bg-gradient-to-b",
        "from-base-100"
    )
    node.classList.add("scroll-shadow")

    parent.insertBefore(container, node)
    container.appendChild(shadow)
    container.appendChild(node)

    const handleScroll = () => {
        if (node.scrollTop > 0) {
            shadow.classList.remove("hidden")
        } else {
            shadow.classList.add("hidden")
        }
    }

    node.addEventListener("scroll", handleScroll)

    return {
        destroy() {
            node.removeEventListener("scroll", handleScroll)
            parent.removeChild(container)
        },
    }
}

type SSParams = { stores: { [key: string]: Writable<number> }; id: string }

export function scrollSync(node: HTMLElement, { stores, id }: SSParams): ActionReturn<SSParams, SSAttrs> {
    if (!(id in stores)) {
        stores[id] = syncedScrollTop()
    }

    const handleScroll = () => {
        stores[id].set(node.scrollTop)
    }

    const unsubscribe = stores[id].subscribe((scrollTop: number) => {
        if (node.scrollTop !== scrollTop) {
            node.scrollTop = scrollTop
        }
    })

    node.addEventListener("scroll", handleScroll)

    return {
        destroy() {
            node.removeEventListener("scroll", handleScroll)
            unsubscribe()
        },
    }
}

export function skeleton(node: HTMLIFrameElement | HTMLImageElement): ActionReturn {
    if (node instanceof HTMLIFrameElement) {
        if (node.contentDocument === null || node.contentDocument.readyState === "complete") {
            return {}
        }
    } else {
        if (node.complete) {
            return {}
        }
    }

    const handler = () => {
        node.classList.remove("skeleton")
    }

    node.classList.add("skeleton")
    node.addEventListener("load", handler)

    return {
        destroy() {
            node.removeEventListener("load", handler)
        },
    }
}
