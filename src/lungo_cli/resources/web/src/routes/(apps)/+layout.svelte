<script lang="ts">
    import { scrollShadow } from "$lib/actions"
    import { NavRail } from "$lib/components"
    import { useStore } from "$lib/utils"

    export let data

    const { currentContainer } = useStore()
</script>

{#if data.apps.length > 0}
    <div class="hidden flex-none md:flex">
        <NavRail />
    </div>
{/if}
<div class="scrollbar-none flex flex-1 overflow-y-auto" bind:this={$currentContainer} use:scrollShadow>
    <slot />
</div>
