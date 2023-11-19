<script lang="ts">
    import { page } from "$app/stores"
    import { safeClick, scrollShadow, scrollSync } from "$lib/actions"
    import { Avatar, SwapIcon } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { LogoutIcon, SettingsIcon } from "$lib/icons"
    import { EIcon } from "$lib/types"
    import { createPlaceholder, useStore } from "$lib/utils"

    const { allowScroll, currentApp, darkTheme, syncedScrollTops } = useStore()

    const handleLogout = async () => {
        await fetch("/logout", {
            method: "POST",
            body: new URLSearchParams({ logoutToken: $page.data.logoutToken }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })

        location.reload()
    }
    const handleSwitchTheme = () => {
        $darkTheme = !$darkTheme
    }

    let checked: boolean | undefined

    $: $allowScroll = !checked
</script>

<header>
    <div class="navbar gap-1.5 p-2">
        <div class="drawer w-12 flex-none">
            <input id="nav-drawer" type="checkbox" class="drawer-toggle" bind:checked />
            <div class="drawer-content">
                <label for="nav-drawer" class="btn btn-circle btn-ghost drawer-button">
                    <span class="h-6 w-6">
                        <SwapIcon icon={EIcon.Menu} active={checked} rotate />
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
                        {#each $page.data.apps as { name, href, icon } (name)}
                            {@const active = $currentApp?.name === name}
                            <li class="mx-0 h-14 w-full rounded-full">
                                <a
                                    class="flex h-full items-center justify-between rounded-full px-5 py-1"
                                    class:!active={active}
                                    {href}
                                >
                                    <span class="h-6 w-6">
                                        <SwapIcon
                                            class={active && $darkTheme === false ? "fill-neutral-content" : ""}
                                            {active}
                                            {icon}
                                        />
                                    </span>
                                    <span class="p-0 text-xs font-semibold">{name}</span>
                                </a>
                            </li>
                        {/each}
                    </ul>
                </div>
            </div>
        </div>
        <div class="flex-1 px-6">
            <a class="text-xl" href="/">{SITE_TITLE}</a>
        </div>
        <div class="mr-1 flex-none">
            <button class="btn btn-circle btn-ghost h-10 min-h-0 w-10" on:click={handleSwitchTheme}>
                <span class="h-6 w-6">
                    <SwapIcon icon={EIcon.Theme} active={$darkTheme} rotate />
                </span>
            </button>
        </div>
        <div class="mr-4 flex-none">
            {#if $page.data.userInfo}
                {@const { email, name } = $page.data.userInfo}
                <div class="dropdown dropdown-end dropdown-bottom">
                    <Avatar button placeholder={createPlaceholder(name.first, name.last)} />
                    <ul class="menu dropdown-content z-20 mt-2 rounded-box bg-base-200 p-2 shadow">
                        <li>
                            <div class="pointer-events-none flex">
                                <Avatar large placeholder={createPlaceholder(name.first, name.last)} />
                                <div class="flex flex-col">
                                    <span class="text-base font-semibold">{name.first} {name.last}</span>
                                    <span>{email}</span>
                                </div>
                            </div>
                        </li>
                        <li><div class="divider menu-title pointer-events-none"></div></li>
                        <li>
                            <a href="/account">
                                <span class="h-6 w-6">
                                    <SettingsIcon />
                                </span>
                                <span>Manage account</span>
                            </a>
                        </li>
                        <li>
                            <button use:safeClick={{ callback: handleLogout }}>
                                <span class="h-6 w-6">
                                    <LogoutIcon />
                                </span>
                                <span>Log out</span>
                            </button>
                        </li>
                    </ul>
                </div>
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
