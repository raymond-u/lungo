<script lang="ts">
    import { onMount } from "svelte"
    // import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()

    const getModifiedUrl = (url: string | URL | null | undefined) => {
        if (typeof url === "string") {
            let [path, query] = url.split("?", 2)

            if (query) {
                if (!query.includes("iframe=1")) {
                    query = "iframe=1&" + query
                }
            } else {
                query = "iframe=1"
            }

            return `${path}?${query}`
        } else if (url instanceof URL) {
            const newUrl = new URL(url.href)

            if (!newUrl.searchParams.has("iframe", "1")) {
                newUrl.searchParams.set("iframe", "1")
            }

            return newUrl.href
        } else {
            return undefined
        }
    }

    const handleLoad = (e: Event) => {
        const iframe = e.target as HTMLIFrameElement
        const pushState = iframe.contentWindow!.history.pushState
        const replaceState = iframe.contentWindow!.history.replaceState

        iframe.contentWindow!.history.pushState = (
            data: Parameters<typeof pushState>[0],
            unused: Parameters<typeof pushState>[1],
            url: Parameters<typeof pushState>[2] = undefined
        ) => {
            console.log("pushState called with url: ", url)
            pushState.call(iframe.contentWindow!.history, data, unused, getModifiedUrl(url))
        }
        iframe.contentWindow!.history.replaceState = (
            data: Parameters<typeof replaceState>[0],
            unused: Parameters<typeof replaceState>[1],
            url: Parameters<typeof replaceState>[2] = undefined
        ) => {
            console.log("replaceState called with url: ", url)
            replaceState.call(iframe.contentWindow!.history, data, unused, getModifiedUrl(url))
        }

        // Object.defineProperty(iframe.contentWindow!.history, "pushState", {
        //     value: (
        //         data: Parameters<typeof history.pushState>[0],
        //         unused: Parameters<typeof history.pushState>[1],
        //         url: Parameters<typeof history.pushState>[2] = undefined
        //     ) => {
        //         console.log("pushState called with url: ", url)
        //
        //         if (url) {
        //             const newUrl = new URL(url)
        //
        //             if (!newUrl.searchParams.has("iframe", "1")) {
        //                 newUrl.searchParams.set("iframe", "1")
        //             }
        //
        //             iframe.contentWindow!.history.pushState(data, unused, newUrl)
        //         } else {
        //             iframe.contentWindow!.history.pushState(data, unused)
        //         }
        //     },
        //     writable: false,
        // })
        // Object.defineProperty(iframe.contentWindow!.history, "replaceState", {
        //     value: (
        //         data: Parameters<typeof history.replaceState>[0],
        //         unused: Parameters<typeof history.replaceState>[1],
        //         url: Parameters<typeof history.replaceState>[2] = undefined
        //     ) => {
        //         console.log("replaceState called with url: ", url)
        //
        //         if (url) {
        //             const newUrl = new URL(url)
        //
        //             if (!newUrl.searchParams.has("iframe", "1")) {
        //                 newUrl.searchParams.set("iframe", "1")
        //             }
        //
        //             iframe.contentWindow!.history.replaceState(data, unused, newUrl)
        //         } else {
        //             iframe.contentWindow!.history.replaceState(data, unused)
        //         }
        //     },
        //     writable: false,
        // })
    }

    let iframe: HTMLIFrameElement | undefined

    onMount(() => {
        iframe!.addEventListener("load", handleLoad)
        iframe!.src = $page.url.pathname + "?iframe=1"

        return () => {
            iframe!.removeEventListener("load", handleLoad)
        }
    })

    // $: if (iframe && iframe.contentWindow) {
    //     goto(iframe.contentWindow.location.pathname, { replaceState: true })
    // }
</script>

<div class="relative z-10 flex-1 overflow-y-auto">
    <iframe title={$currentApp?.name ?? ""} class="h-full w-full" bind:this={iframe} />
</div>
