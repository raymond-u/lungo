<script lang="ts">
    import { navigating } from "$app/stores"

    let showLoading = false
    let timer: ReturnType<typeof setTimeout>

    $: if ($navigating) {
        timer = setTimeout(() => {
            showLoading = true
        }, 500)
    } else {
        clearTimeout(timer)
        showLoading = false
    }
</script>

{#if $navigating && showLoading}
    <div>
        <dialog class="modal modal-open">
            <div class="modal-box flex w-auto items-center justify-center">
                <span class="loading loading-bars loading-lg"></span>
            </div>
        </dialog>
    </div>
{/if}
