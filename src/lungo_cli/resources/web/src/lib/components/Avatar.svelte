<script lang="ts">
    export let button = false
    export let large = false
    export let placeholder: string | undefined = undefined
</script>

{#if button}
    <button
        class="inline-flex items-center justify-center rounded-full bg-accent font-bold text-accent-content {large
            ? 'h-10 w-10 text-lg'
            : 'h-8 w-8 text-sm'}"
    >
        {placeholder ?? ""}
    </button>
{:else}
    <span
        class="inline-flex items-center justify-center rounded-full bg-accent font-bold text-accent-content {large
            ? 'h-10 w-10 text-lg'
            : 'h-8 w-8 text-sm'}"
    >
        {placeholder ?? ""}
    </span>
{/if}
