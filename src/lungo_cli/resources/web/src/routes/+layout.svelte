<script lang="ts">
    import "../app.pcss"
    import { onMount } from "svelte"
    import { page } from "$app/stores"
    import { AppShell, LoadingIndicator } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { ETheme } from "$lib/types"
    import { createStore, getPageTitle } from "$lib/utils"

    const { allowScroll, currentTheme, isSafari } = createStore()

    let title: string
    let canonicalUrl: string

    onMount(() => {
        const theme = localStorage.getItem("theme")
        $currentTheme = theme && Object.values(ETheme).includes(theme as ETheme) ? (theme as ETheme) : ETheme.Auto
        $isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
    })

    $: title = getPageTitle($page.data.title)
    $: canonicalUrl = $page.url.origin + $page.url.pathname
</script>

<div>
    <LoadingIndicator />
    <AppShell>
        <slot />
    </AppShell>
</div>

<svelte:head>
    <title>{title}</title>
    <meta name="title" content={title} />
    <meta name="description" content="Welcome to {SITE_TITLE}." />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content={title} />
    <meta property="og:description" content="Welcome to {SITE_TITLE}." />
    <meta property="og:url" content={canonicalUrl} />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content="Welcome to {SITE_TITLE}." />
    <meta name="twitter:url" content={canonicalUrl} />

    {#if !$allowScroll}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>
