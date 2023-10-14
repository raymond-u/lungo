<script lang="ts">
    import { HeroFrame } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { getRandomElement, getTitle } from "$lib/utils"

    export let data

    const quotes = [
        "a dance of flavors",
        "a hug in a mug",
        "a masterpiece in each pour",
        "a poetry of aroma",
        "a quiet solitude",
        "a whisper of inspiration",
    ]
</script>

<svelte:head>
    <title>{getTitle("Home")}</title>
</svelte:head>

<HeroFrame>
    <div class="hero h-full">
        <div class="hero-content flex-col gap-32 lg:flex-row-reverse">
            <img src="./cover.jpg" alt="cover" class="max-w-xs rounded-2xl shadow-2xl" />
            <div>
                {#if data.userInfo}
                    {@const { name } = data.userInfo}
                    <h1 class="text-4xl font-bold">Welcome, {name.first} {name.last}</h1>
                    <p class="pt-4 text-lg">{getRandomElement(quotes)}</p>
                {:else}
                    <h1 class="text-4xl font-bold">Welcome to {SITE_TITLE}</h1>
                    <p class="pb-20 pt-4 text-lg">{getRandomElement(quotes)}</p>
                    <a class="btn btn-primary" href="/login">Sign in</a>
                {/if}
            </div>
        </div>
    </div>
</HeroFrame>
