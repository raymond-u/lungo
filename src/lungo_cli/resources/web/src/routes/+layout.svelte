<script lang="ts">
    import "../app.pcss"
    import { onMount } from "svelte"
    import { page } from "$app/stores"
    import { LoadingIndicator, NavBar } from "$lib/components"
    import { createStore, getTitleFromSlug } from "$lib/utils"

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
    <header>
        <div class="h-16">
            <NavBar />
        </div>
    </header>
    <main>
        <div class="flex h-[calc(100vh-4rem)]">
            <slot />
        </div>
    </main>
</div>

<svelte:head>
    <title>{getTitleFromSlug($page.data.title)}</title>
    {#if !$allowScroll}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>
