<script lang="ts">
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()
    const src = $page.url.pathname + "?iframe=1"

    let iframe: HTMLIFrameElement | undefined

    $: {
        console.log("###")
        console.log("Href changed to: " + iframe?.contentWindow?.location.href)
        console.log("Referer changed to: " + iframe?.contentDocument?.referrer)
        console.log("History changed to: " + iframe?.contentWindow?.history.state)
    }

    // $: if (iframe && iframe.contentWindow) {
    //     goto(iframe.contentWindow.location.pathname, { replaceState: true })
    // }
</script>

<div class="relative flex-1 overflow-y-auto px-6 py-12">
    {#if $currentApp}
        <iframe {src} title={$currentApp.name} class="h-full w-full" bind:this={iframe} />
    {/if}
</div>
