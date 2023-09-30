<script lang="ts">
    import { page } from "$app/stores"
    import { syncScroll } from "$lib/actions"
    import { SITE_TITLE } from "$lib/constants"
    import { Icon } from "$lib/components"
    import { EIcon } from "$lib/types"
    import { useStore } from "$lib/utils"

    const { allowScroll, currentApp, syncedScrollTops } = useStore()
    let checked: boolean | undefined

    $: $allowScroll = !checked
</script>

<div class="navbar gap-1.5 bg-base-100 px-4 py-2">
    <div class="drawer w-12 flex-none">
        <input id="nav-drawer" type="checkbox" class="drawer-toggle" bind:checked />
        <div class="drawer-content">
            <label for="nav-drawer" class="btn btn-circle btn-ghost drawer-button h-12 w-12">
                <span class="h-6 w-6">
                    <Icon icon={EIcon.Menu} active={checked} rotate />
                </span>
            </label>
        </div>
        <div class="drawer-side top-16 z-10 h-[calc(100vh-4rem)]">
            <label for="nav-drawer" class="drawer-overlay"></label>
            <div class="pointer-events-none absolute z-10 h-12 w-80 bg-gradient-to-b from-base-100"></div>
            <div
                class="scrollbar-none h-full w-80 overflow-y-auto bg-base-100 py-10"
                use:syncScroll={{ id: "nav", stores: syncedScrollTops }}
            >
                <ul class="menu items-center gap-2 p-2 pb-3">
                    {#each $page.data.apps as { name, href, icon } (name)}
                        {@const active = $currentApp?.name === name}
                        <li class="mx-0 h-14 w-full rounded-full">
                            <a
                                class="flex h-full items-center justify-between rounded-full px-5 py-1"
                                class:active
                                {href}
                            >
                                <span class="h-6 w-6">
                                    <Icon {active} {icon} />
                                </span>
                                <span class="p-0 text-xs font-semibold">{name}</span>
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    </div>
    <div class="flex-1 px-2">
        <a class="text-xl" href="/">{SITE_TITLE}</a>
    </div>
    <div class="flex-none">
        <div class="avatar placeholder">
            <div class="w-8 rounded-full bg-accent text-accent-content">
                <a class="p-1 text-sm font-bold" href="/">RU</a>
            </div>
        </div>
    </div>
</div>
<div
    class="pointer-events-none absolute left-0 right-4 z-10 h-12 bg-gradient-to-b from-base-100"
    class:opacity-0={checked}
></div>
