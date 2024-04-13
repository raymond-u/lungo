<script lang="ts">
    import { scrollShadow } from "$lib/actions"
    import { useStore } from "$lib/utils"

    const { currentContainer } = useStore()
</script>

<div class="scrollbar-none flex flex-1 overflow-y-auto" bind:this={$currentContainer} use:scrollShadow>
    <slot />
</div>
