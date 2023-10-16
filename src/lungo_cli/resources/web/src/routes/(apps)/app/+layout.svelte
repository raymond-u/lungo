<script lang="ts">
    import { onMount } from "svelte"
    // import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()

    const handleLoad = () => {
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
    {#if $currentApp}
        <iframe title={$currentApp.name} class="h-full w-full" bind:this={iframe} />
    {/if}
    <slot />
</div>
