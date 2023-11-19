<script lang="ts">
    import "../app.pcss"
    import { onMount } from "svelte"
    import { page } from "$app/stores"
    import { AppShell, LoadingIndicator } from "$lib/components"
    import { createStore, createTitle } from "$lib/utils"

    const { allowScroll, darkTheme } = createStore()

    const observeThemeChange = (e: MediaQueryListEvent) => {
        $darkTheme = e.matches
    }

    onMount(() => {
        if (window.matchMedia) {
            $darkTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
            window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", observeThemeChange)

            return () => {
                window.matchMedia("(prefers-color-scheme: dark)").removeEventListener("change", observeThemeChange)
            }
        }
    })
</script>

<div data-theme={typeof $darkTheme === "undefined" ? undefined : $darkTheme ? "dark" : "light"}>
    <LoadingIndicator />
    <AppShell>
        <slot />
    </AppShell>
</div>

<svelte:head>
    <title>{createTitle($page.data.title)}</title>
    {#if !$allowScroll}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>
