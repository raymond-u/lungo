<script lang="ts">
    import { scrollShadow } from "$lib/actions"
    import { NavRail } from "$lib/components"

    export let data
</script>

{#if data.apps.length > 0}
    <div class="hidden flex-none md:flex">
        <NavRail />
    </div>
{/if}
<div class="scrollbar-transparent flex flex-1 overflow-y-auto" use:scrollShadow>
    <slot />
</div>
