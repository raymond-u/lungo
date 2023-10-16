<script lang="ts">
    import { onMount } from "svelte"
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()

    const src = $page.url.pathname + "?iframe=1"

    let iframe: HTMLIFrameElement | undefined

    onMount(() => {
        Object.defineProperty(iframe!.contentWindow!.history, "pushState", {
            value: (
                data: Parameters<typeof history.pushState>[0],
                unused: Parameters<typeof history.pushState>[1],
                url: Parameters<typeof history.pushState>[2] = undefined
            ) => {
                if (url) {
                    let newUrl = new URL(url)

                    if (!newUrl.searchParams.has("iframe", "1")) {
                        newUrl.searchParams.set("iframe", "1")
                    }

                    iframe!.contentWindow!.history.pushState(data, unused, newUrl)
                } else {
                    iframe!.contentWindow!.history.pushState(data, unused)
                }
            },
            writable: false,
        })
        Object.defineProperty(iframe!.contentWindow!.history, "replaceState", {
            value: (
                data: Parameters<typeof history.replaceState>[0],
                unused: Parameters<typeof history.replaceState>[1],
                url: Parameters<typeof history.replaceState>[2] = undefined
            ) => {
                if (url) {
                    let newUrl = new URL(url)

                    if (!newUrl.searchParams.has("iframe", "1")) {
                        newUrl.searchParams.set("iframe", "1")
                    }

                    iframe!.contentWindow!.history.replaceState(data, unused, newUrl)
                } else {
                    iframe!.contentWindow!.history.replaceState(data, unused)
                }
            },
            writable: false,
        })
    })

    // $: if (iframe && iframe.contentWindow) {
    //     goto(iframe.contentWindow.location.pathname, { replaceState: true })
    // }
</script>

<div class="relative flex-1 overflow-y-auto px-6 py-12">
    {#if $currentApp}
        <iframe {src} title={$currentApp.name} class="h-full w-full" bind:this={iframe} />
    {/if}
</div>
