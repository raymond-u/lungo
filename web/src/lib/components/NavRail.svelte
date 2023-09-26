<script lang="ts">
    import { page } from "$app/stores"
    import { syncScroll } from "$lib/actions"
    import Icon from "$lib/components/Icon.svelte"
    import { useStore } from "$lib/utils"

    const { currentApp, syncedScrollTops } = useStore()
</script>

<nav class="scrollbar-none w-20 overflow-y-auto py-10" use:syncScroll={{ id: "nav", stores: syncedScrollTops }}>
    <ul class="menu items-center gap-1 px-3 py-2">
        {#each $page.data.apps as { name, href, icon } (name)}
            {@const active = $currentApp?.name === name}
            <li class="mt-3 h-8 w-14 transition" class:-translate-y-3={active}>
                <a class="rounded-full py-1" class:active {href}>
                    <Icon {active} {icon} />
                </a>
            </li>
            <li
                class="pointer-events-none -mt-7 mb-4 py-1 transition"
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
