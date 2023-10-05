<script lang="ts">
    import { page } from "$app/stores"
    import { HeroFrame } from "$lib/components"
</script>

<HeroFrame>
    <div class="hero h-full">
        <div class="hero-content text-center">
            <div class="max-w-md">
                <h1 class="text-2xl font-bold">Error {$page.status}: {$page.error?.message ?? "Unknown error"}</h1>
            </div>
        </div>
    </div>
</HeroFrame>
