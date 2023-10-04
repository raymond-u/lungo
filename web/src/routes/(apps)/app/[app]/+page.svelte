<script lang="ts">
    import { getTitle, useStore } from "$lib/utils"

    const { currentApp } = useStore()
</script>

<div class="flex-1 overflow-y-auto px-6 py-12">
    {#if $currentApp}
        <p>
            You can access.
            {#each Array(100).keys() as i (i)}
                <br />
                {i}: You can use HTML tags in Svelte. Yeah you can use HTML tags in Svelte.
            {/each}
        </p>
    {:else}
        <p>You cannot access.</p>
    {/if}
</div>

<svelte:head>
    <title>{getTitle($currentApp?.name ?? "?")}</title>
</svelte:head>
