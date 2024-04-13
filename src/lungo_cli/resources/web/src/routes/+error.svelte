<script lang="ts">
    import { page } from "$app/stores"
    import { HeroFrame } from "$lib/components"
</script>

<HeroFrame>
    <div class="hero h-full">
        <div class="hero-content text-balance text-center">
            <div class="flex max-w-lg flex-col md:max-w-xl">
                {#if $page.status === 429}
                    <h1 class="my-6 text-4xl font-bold">Hey, you're going too fast!</h1>
                    <a class="link text-lg" href="/">Let's take a break.</a>
                {:else if String($page.status).startsWith("4")}
                    <h1 class="my-6 text-4xl font-bold">Seems like you're lost...</h1>
                    <a class="link text-lg" href="/">Let's not stuck here forever.</a>
                {:else}
                    <h1 class="my-6 text-4xl font-bold">Oops, something went wrong...</h1>
                    <a class="link text-lg" href="/">Let's get you back on track.</a>
                {/if}
            </div>
        </div>
    </div>
</HeroFrame>
