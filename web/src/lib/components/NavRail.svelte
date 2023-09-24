<script lang="ts">
    import { page } from "$app/stores"
    import Icon from "$lib/components/Icon.svelte"
    import { useStore } from "$lib/utils"

    const { currentApp, navExpanded, navScrollTop } = useStore()
    const handleScroll = (e: Event) => {
        const target = e.target as HTMLElement
        $navScrollTop = target.scrollTop
    }

    let scrollable: HTMLElement | undefined

    $: if (!$navExpanded) {
        if (scrollable) {
            scrollable.scrollTop = $navScrollTop
        }
    }
</script>

<nav bind:this={scrollable} class="scrollbar-none w-20 overflow-y-auto py-10" on:scroll={handleScroll}>
    <ul class="menu items-center gap-1 px-3 py-2">
        {#each $page.data.apps as { name, href, icon }}
            {@const active = $currentApp?.name === name}
            <li class="mt-3 h-8 w-14 transition duration-200" class:-translate-y-3={active}>
                <a class="rounded-full py-1" class:active {href}>
                    <Icon {active} {icon} />
                </a>
            </li>
            <li
                class="pointer-events-none -mt-7 mb-4 py-1 transition duration-200"
                class:translate-y-4={active}
                class:opacity-0={!active}
            >
                <span class="p-0 text-xs font-semibold">
                    {name}
                </span>
            </li>
        {/each}
    </ul>
</nav>
