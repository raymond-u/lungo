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

        iframe.contentWindow!.addEventListener("unload", handleUnload)

        console.log("iframe loaded with url: ", iframe.contentWindow!.location.href)

        goto(getOriginalUrl(iframe.contentWindow!.location.href), { replaceState: true })

        iframe.contentWindow!.history.pushState = (
            data: Parameters<typeof pushState>[0],
            unused: Parameters<typeof pushState>[1],
            url: Parameters<typeof pushState>[2] = undefined
        ) => {
            console.log("pushState called with url: ", url)

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
            console.log("replaceState called with url: ", url)

            if (url) {
                goto(getOriginalUrl(url), { replaceState: true })
                replaceState.call(iframe.contentWindow!.history, data, unused, getModifiedUrl(url))
            } else {
                replaceState.call(iframe.contentWindow!.history, data, unused)
            }
        }
    }

    const handleUnload = (e: Event) => {
        const iframe = e.target as HTMLIFrameElement
        console.log("iframe unloaded with url: ", iframe.contentWindow?.location.href)
        setTimeout(() => {
            console.log("timeout 0 iframe unloaded with url: ", iframe.contentWindow?.location.href)
        }, 0)
    }

    let iframe: HTMLIFrameElement | undefined

    onMount(() => {
        iframe!.addEventListener("load", handleLoad)

        console.log(
            "before assign a src",
            iframe!.contentWindow?.location.href,
            iframe!.contentWindow === undefined || iframe!.contentWindow === null
        )

        try {
            iframe!.contentWindow!.addEventListener("unload", handleUnload)
        } catch (e) {
            console.log("error", e)
        }

        iframe!.src = $page.url.pathname + "?iframe=1"

        console.log(
            "after assign a src",
            iframe!.contentWindow?.location.href,
            iframe!.contentWindow === undefined || iframe!.contentWindow === null
        )

        try {
            iframe!.contentWindow!.addEventListener("unload", handleUnload)
        } catch (e) {
            console.log("error", e)
        }

        setTimeout(() => {
            console.log(
                "timeout 0 iframe with url: ",
                iframe!.contentWindow?.location.href,
                iframe!.contentWindow === undefined || iframe!.contentWindow === null
            )
            iframe!.contentWindow!.addEventListener("unload", handleUnload)
        }, 0)

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
