<script lang="ts">
    import { page } from "$app/stores"
    import { scrollShadow, scrollSync } from "$lib/actions"
    import { SwappableIcon } from "$lib/components"
    import { truncate, useAppIcon, useStore } from "$lib/utils"

    const { currentApp, darkTheme, syncedScrollTops } = useStore()
</script>

<nav
    class="scrollbar-none w-16 overflow-y-auto py-10"
    use:scrollShadow
    use:scrollSync={{ id: "nav", stores: syncedScrollTops }}
>
    <ul class="menu items-center gap-1 px-0 py-2">
        {#each $page.data.apps as { name, descriptiveName, href } (name)}
            {@const active = $currentApp?.name === name}
            {@const { icon, altIcon } = useAppIcon(name)}
            <li class="mt-3 h-8 w-14 transition" class:-translate-y-3={active}>
                <a class="rounded-full py-1" class:!active={active} {href}>
                    <SwappableIcon
                        class={active && $darkTheme === false ? "fill-neutral-content" : ""}
                        {icon}
                        {altIcon}
                        altIconActive={active}
                    />
                </a>
            </li>
            <li
                class="pointer-events-none -mt-7 mb-4 py-1 transition"
                class:translate-y-4={active}
                class:opacity-0={!active}
            >
                <span class="p-0 text-xs font-semibold">
                    {truncate(descriptiveName, 8)}
                </span>
            </li>
        {/each}
    </ul>
</nav>
