<script lang="ts">
    import { page } from "$app/stores"
    import { SITE_TITLE } from "$lib/constants.js"
    import Icon from "$lib/components/Icon.svelte"
    import { EIcon } from "$lib/types.js"
    import { useStore } from "$lib/utils"

    const { currentApp, navExpanded, navScrollTop } = useStore()
    const handleScroll = (e: Event) => {
        const target = e.target as HTMLDivElement
        $navScrollTop = target.scrollTop
    }

    let checked: boolean | undefined
    let scrollable: HTMLDivElement | undefined

    $: $navExpanded = checked ?? false

    $: if (checked) {
        if (scrollable) {
            scrollable.scrollTop = $navScrollTop
        }
    }
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
        <div class="drawer-side top-16 z-10 h-[calc(100vh-64px)]">
            <label for="nav-drawer" class="drawer-overlay"></label>
            <div
                bind:this={scrollable}
                class="scrollbar-none h-full w-80 overflow-y-auto bg-base-100 py-10"
                on:scroll={handleScroll}
            >
                <ul class="menu items-center gap-2 p-2 pb-3">
                    {#each $page.data.apps as { name, href, icon }}
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
        <a
            class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-accent text-sm font-bold text-accent-content"
            href="/"
        >
            RU
        </a>
    </div>
</div>
<div class="absolute left-20 right-4 h-12 bg-gradient-to-b from-base-100"></div>
