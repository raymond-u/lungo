<script lang="ts">
    import { NavRail } from "$lib/components"

    export let data
</script>

{#if data.apps.length > 0}
    <div class="flex flex-none">
        <NavRail />
    </div>
{/if}
<div class="flex flex-1">
    <slot />
</div>
