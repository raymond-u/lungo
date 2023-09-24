<script lang="ts">
    import { formatTitle, useStore } from "$lib/utils"

    const { currentApp } = useStore()
</script>

<div class="flex-1 overflow-y-auto">
    {#if $currentApp}
        <p>
            You can access.
            {@html "<br>You can use HTML tags in Svelte. Yeah you can use HTML tags in Svelte.".repeat(50)}
        </p>
    {:else}
        <p>You cannot access.</p>
    {/if}
</div>

<svelte:head>
    <title>{formatTitle($currentApp?.name ?? "?")}</title>
</svelte:head>
