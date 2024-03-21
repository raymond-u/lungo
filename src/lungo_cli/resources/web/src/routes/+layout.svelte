<script lang="ts">
    import "../app.pcss"
    import { onMount } from "svelte"
    import { page } from "$app/stores"
    import { AppShell, LoadingIndicator } from "$lib/components"
    import { ETheme } from "$lib/types"
    import { createStore, usePageTitle } from "$lib/utils"

    const { allowScroll, currentTheme, isSafari } = createStore()

    onMount(() => {
        const theme = localStorage.getItem("theme")
        $currentTheme = theme && Object.values(ETheme).includes(theme as ETheme) ? (theme as ETheme) : ETheme.Auto

        // @ts-expect-error exists for Safari on macOS
        $isSafari = window.safari !== undefined
    })
</script>

<div>
    <LoadingIndicator />
    <AppShell>
        <slot />
    </AppShell>
</div>

<svelte:head>
    <title>{usePageTitle($page.data.title)}</title>
    {#if !$allowScroll}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>
