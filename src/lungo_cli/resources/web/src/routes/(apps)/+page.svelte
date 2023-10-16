<script lang="ts">
    import { HeroFrame } from "$lib/components"
    import { SITE_SUBTITLE, SITE_TITLE } from "$lib/constants"
    import { getRandomElement } from "$lib/utils"

    export let data

    const subtitle = getRandomElement(JSON.parse(SITE_SUBTITLE))
</script>

<HeroFrame>
    <div class="hero h-full">
        <div class="hero-content flex-col gap-32 lg:flex-row-reverse">
            <img src="/cover.jpg" alt="cover" class="w-80 rounded-2xl shadow-2xl" />
            <div>
                {#if data.userInfo}
                    {@const { name } = data.userInfo}
                    <h1 class="text-4xl font-bold">Welcome, {name.first} {name.last}</h1>
                    <p class="pt-4 text-lg">{subtitle}</p>
                {:else}
                    <h1 class="text-4xl font-bold">Welcome to {SITE_TITLE}</h1>
                    <p class="pb-20 pt-4 text-lg">{subtitle}</p>
                    <a class="btn btn-primary" href="/login">Sign in</a>
                {/if}
            </div>
        </div>
    </div>
</HeroFrame>
