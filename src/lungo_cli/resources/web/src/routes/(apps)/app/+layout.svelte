<script lang="ts">
    import { onMount } from "svelte"
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()

    const getOriginalUrl = (url: string | URL) => {
        if (typeof url === "string") {
            const [path, query] = url.split("?", 2)
            const params = new URLSearchParams(query)
            params.delete("iframe", "1")

            if (params.size > 0) {
                return `${path}?${params.toString()}`
            }

            return path
        } else {
            const newUrl = new URL(url.href)
            newUrl.searchParams.delete("iframe", "1")

            return newUrl.href
        }
    }

    const getModifiedUrl = (url: string | URL) => {
        if (typeof url === "string") {
            const [path, query] = url.split("?", 2)
            const params = new URLSearchParams(query)
            params.set("iframe", "1")

            return `${path}?${params.toString()}`
        } else {
            const newUrl = new URL(url.href)
            newUrl.searchParams.set("iframe", "1")

            return newUrl.href
        }
    }

    const handleLoad = (e: Event) => {
        const iframe = e.target as HTMLIFrameElement
        const pushState = iframe.contentWindow!.history.pushState
        const replaceState = iframe.contentWindow!.history.replaceState

        if (!iframe.contentWindow!.location.search.includes("iframe=1")) {
            iframe.contentWindow!.history.replaceState(null, "", getModifiedUrl(iframe.contentWindow!.location.href))
        }

        goto(getOriginalUrl(iframe.contentWindow!.location.href), { replaceState: true })

        iframe.contentWindow!.history.pushState = (
            data: Parameters<typeof pushState>[0],
            unused: Parameters<typeof pushState>[1],
            url: Parameters<typeof pushState>[2] = undefined
        ) => {
            if (url) {
                goto(getOriginalUrl(url), { replaceState: true })
                pushState.call(iframe.contentWindow!.history, data, unused, getModifiedUrl(url))
            } else {
                pushState.call(iframe.contentWindow!.history, data, unused)
            }
        }
        iframe.contentWindow!.history.replaceState = (
            data: Parameters<typeof replaceState>[0],
            unused: Parameters<typeof replaceState>[1],
            url: Parameters<typeof replaceState>[2] = undefined
        ) => {
            if (url) {
                goto(getOriginalUrl(url), { replaceState: true })
                replaceState.call(iframe.contentWindow!.history, data, unused, getModifiedUrl(url))
            } else {
                replaceState.call(iframe.contentWindow!.history, data, unused)
            }
        }
    }

    let iframe: HTMLIFrameElement | undefined

    onMount(() => {
        iframe!.addEventListener("load", handleLoad)
        iframe!.src = $page.url.pathname + "?iframe=1"

        const unsubscribe = currentApp.subscribe((value) => {
            if (value) {
                if (!iframe!.src.match(`^(?:https?://[^/]+)?${value.href}`)) {
                    iframe!.src = value.href + "?iframe=1"
                }
            }
        })

        return () => {
            unsubscribe()
            iframe!.removeEventListener("load", handleLoad)
        }
    })
</script>

<div class="relative z-10 flex-1 overflow-y-auto">
    <iframe title={$currentApp?.name ?? ""} class="h-full w-full" bind:this={iframe} />
    <slot />
</div>
