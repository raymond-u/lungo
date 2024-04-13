<script lang="ts">
    import { skeleton } from "$lib/actions"
    import CoverImage from "$lib/assets/cover.jpg?enhanced"
    import { HeroFrame } from "$lib/components"
    import { SITE_SUBTITLE, SITE_TITLE } from "$lib/constants"
    import { getRandomElement } from "$lib/utils"

    export let data

    const subtitle = getRandomElement(JSON.parse(SITE_SUBTITLE) as string[])
</script>

<HeroFrame>
    <div class="hero h-full">
        <div class="hero-content flex-col gap-16 lg:flex-row-reverse lg:gap-32">
            <enhanced:img
                class="max-h-48 w-80 rounded-box object-cover shadow-2xl lg:max-h-none"
                src={CoverImage}
                alt="cover"
                use:skeleton
            />
            <div>
                {#if data.userInfo}
                    <h1 class="text-4xl font-bold">Welcome back, {data.userInfo.name.first}</h1>
                    <p class="pt-4 text-lg">{subtitle}</p>
                {:else}
                    <h1 class="text-4xl font-bold">Welcome to {SITE_TITLE}</h1>
                    <p class="pb-10 pt-4 text-lg lg:pb-20">{subtitle}</p>
                    <a class="btn btn-primary" href="/login">Sign in</a>
                {/if}
            </div>
        </div>
    </div>
</HeroFrame>
