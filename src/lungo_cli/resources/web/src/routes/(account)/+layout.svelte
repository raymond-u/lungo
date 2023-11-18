<script lang="ts">
    import { scrollShadow } from "$lib/actions"
</script>

<div class="scrollbar-transparent flex flex-1 overflow-y-auto" use:scrollShadow>
    <slot />
</div>
