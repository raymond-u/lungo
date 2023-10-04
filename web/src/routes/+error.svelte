<script>
    import { page } from "$app/stores"
</script>

<div class="px-6 py-12">
    <span class="text-xl">
        {$page.status}: {$page.error?.message ?? "Unknown error"}
    </span>
</div>
