<script lang="ts">
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { useStore } from "$lib/utils"

    const { currentApp } = useStore()
    const src = $page.url.pathname + "?iframe=1"

    let iframe: HTMLIFrameElement | undefined

    $: if (iframe && iframe.contentWindow) {
        goto(iframe.contentWindow.location.pathname, { replaceState: true })
    }
</script>

<div class="flex-1 overflow-y-auto px-6 py-12">
    {#if $currentApp}
        <iframe {src} title={$currentApp.name} class="h-full w-full" bind:this={iframe} />
    {/if}
</div>
