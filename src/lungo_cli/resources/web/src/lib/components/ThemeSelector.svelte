<script lang="ts">
    import { SwappableIcon } from "$lib/components"
    import { CheckIcon, ExpandIcon } from "$lib/icons"
    import { EIcon, ETheme } from "$lib/types"
    import { useStore } from "$lib/utils"

    const { currentTheme, darkTheme } = useStore()

    const handleSelectTheme = (theme: ETheme) => {
        return () => {
            $currentTheme = theme
            localStorage.setItem("theme", theme)
        }
    }

    const handleSwitchTheme = () => {
        if ($darkTheme) {
            handleSelectTheme(ETheme.Light)()
        } else {
            handleSelectTheme(ETheme.Dark)()
        }
    }
</script>

<div class="flex items-center">
    <button class="btn btn-circle btn-ghost h-10 min-h-0 w-10" on:click={handleSwitchTheme}>
        <span class="h-6 w-6">
            <SwappableIcon icon={EIcon.Theme} active={$darkTheme} rotate>
                <input class="theme-controller" type="checkbox" value="dark" />
            </SwappableIcon>
        </span>
    </button>
    <div class="dropdown dropdown-end dropdown-bottom flex items-center">
        <button class="h-6 w-6">
            <ExpandIcon />
        </button>
        <ul
            class="scrollbar-transparent dropdown-content z-20 mt-2 flex max-h-80 flex-col gap-2 overflow-y-auto rounded-btn bg-base-200 p-2 shadow"
        >
            {#each Object.entries(ETheme) as [key, value] (value)}
                <li>
                    <div
                        class="relative flex gap-1 rounded-btn bg-base-100 text-base-content"
                        data-theme={value === ETheme.Auto ? undefined : value}
                    >
                        <input
                            type="radio"
                            name="theme-dropdown"
                            class="peer theme-controller btn btn-ghost btn-sm h-12 flex-1 justify-start border-0 pl-12 pr-20 checked:bg-transparent"
                            aria-label={key}
                            checked={$currentTheme === value}
                            {value}
                            on:click={handleSelectTheme(value)}
                        />
                        <span class="pointer-events-none absolute left-3 top-3 hidden h-6 w-6 peer-checked:inline">
                            <CheckIcon />
                        </span>
                        {#if value !== ETheme.Auto}
                            <div class="pointer-events-none absolute right-3 top-3 flex h-6 gap-1">
                                <span class="w-2 rounded-full bg-primary"></span>
                                <span class="w-2 rounded-full bg-secondary"></span>
                                <span class="w-2 rounded-full bg-accent"></span>
                            </div>
                        {/if}
                    </div>
                </li>
            {/each}
        </ul>
    </div>
</div>
