<script lang="ts">
    import "../app.pcss"
    import NavBar from "$lib/components/NavBar.svelte"
    import { createStore } from "$lib/utils"

    const { allowScroll } = createStore()
</script>

<header>
    <div class="h-16">
        <NavBar />
    </div>
</header>
<main>
    <div class="flex h-[calc(100vh-64px)]">
        <slot />
    </div>
</main>

<svelte:head>
    {#if !$allowScroll}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>
