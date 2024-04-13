<script lang="ts">
    import { page } from "$app/stores"
    import { scrollShadow, scrollSync } from "$lib/actions"
    import { SwappableIcon, ThemeSelector } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { CloseIcon, FullscreenIcon, MenuIcon } from "$lib/icons"
    import { getNameInitials, useAppIcon, useStore } from "$lib/utils"
    import AccountDropdown from "./AccountDropdown.svelte"

    const { allowScroll, currentApp, currentIFrame, darkTheme, isSafari, syncedScrollTops } = useStore()

    const handleFullscreen = () => {
        $currentIFrame?.requestFullscreen()
    }

    let checked: boolean | undefined

    $: $allowScroll = !checked
</script>

<header>
    <div class="navbar gap-3 p-2">
        <div class="drawer w-12 flex-none">
            <input id="nav-drawer" type="checkbox" class="drawer-toggle" bind:checked />
            <div class="drawer-content">
                <label for="nav-drawer" class="btn btn-circle btn-ghost drawer-button">
                    <span class="h-6 w-6">
                        <SwappableIcon icon={MenuIcon} altIcon={CloseIcon} altIconActive={checked} rotate />
                    </span>
                </label>
            </div>
            <div class="drawer-side top-16 z-20 h-[calc(100vh-4rem)]">
                <label for="nav-drawer" class="drawer-overlay"></label>
                <div
                    class="scrollbar-none h-[calc(100vh-4rem)] w-80 overflow-y-auto bg-base-100 py-10"
                    use:scrollShadow
                    use:scrollSync={{ id: "nav", stores: syncedScrollTops }}
                >
                    <ul class="menu items-center gap-2 p-2 pb-3">
                        {#each $page.data.apps as { name, descriptiveName, href } (name)}
                            {@const active = $currentApp?.name === name}
                            {@const { icon, altIcon } = useAppIcon(name)}
                            <li class="mx-0 h-14 w-full rounded-full">
                                <a
                                    class="flex h-full items-center justify-between rounded-full px-5 py-1"
                                    class:!active={active}
                                    {href}
                                >
                                    <span class="h-6 w-6">
                                        <SwappableIcon
                                            class={active && $darkTheme === false ? "fill-neutral-content" : ""}
                                            {icon}
                                            {altIcon}
                                            altIconActive={active}
                                        />
                                    </span>
                                    <span class="p-0 text-xs font-semibold">{descriptiveName}</span>
                                </a>
                            </li>
                        {/each}
                    </ul>
                </div>
            </div>
        </div>
        <div class="flex-1 px-4">
            <a class="text-xl" href="/">{SITE_TITLE}</a>
        </div>
        {#if $currentIFrame}
            <div class="hidden flex-none md:flex">
                <button class="btn btn-circle btn-ghost h-10 min-h-0 w-10" on:click={handleFullscreen}>
                    <span class="h-6 w-6">
                        <FullscreenIcon />
                    </span>
                </button>
            </div>
        {/if}
        <div class="flex-none">
            <ThemeSelector />
        </div>
        <div class="ml-2 mr-4 flex-none">
            {#if $page.data.userInfo}
                {@const { email, name } = $page.data.userInfo}
                {#if $isSafari}
                    <details class="dropdown dropdown-end dropdown-bottom">
                        <summary
                            class="inline-flex h-8 w-8 cursor-pointer items-center justify-center rounded-full bg-accent text-sm font-bold text-accent-content"
                        >
                            {getNameInitials(name.first, name.last)}
                        </summary>
                        <AccountDropdown {email} firstName={name.first} lastName={name.last} />
                    </details>
                {:else}
                    <div class="dropdown dropdown-end dropdown-bottom">
                        <button
                            class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-accent text-sm font-bold text-accent-content"
                        >
                            {getNameInitials(name.first, name.last)}
                        </button>
                        <AccountDropdown {email} firstName={name.first} lastName={name.last} />
                    </div>
                {/if}
            {:else}
                <a class="btn" href="/login">Sign in</a>
            {/if}
        </div>
    </div>
</header>
<main>
    <div class="flex h-[calc(100vh-4rem)]">
        <slot />
    </div>
</main>
