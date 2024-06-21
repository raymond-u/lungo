<script lang="ts">
    export let stretched = false
    export let wrapped = false
</script>

<div class="flex size-full flex-col items-center">
    <div class="flex w-full flex-1 items-center justify-center py-16">
        {#if wrapped}
            <div
                class="flex max-w-md flex-1 flex-col items-center justify-center gap-4 rounded-box bg-base-200 px-12 py-16"
                class:md:max-w-lg={stretched}
            >
                <slot />
            </div>
        {:else}
            <slot />
        {/if}
    </div>
</div>
