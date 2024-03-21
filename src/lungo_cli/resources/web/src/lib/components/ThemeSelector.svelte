<script lang="ts">
    import { SwappableIcon } from "$lib/components"
    import { DarkModeIcon, ExpandIcon, LightModeIcon } from "$lib/icons"
    import { ETheme } from "$lib/types"
    import { useStore } from "$lib/utils"
    import ThemeSelectorDropdown from "./ThemeSelectorDropdown.svelte"

    const { currentTheme, darkTheme, isSafari } = useStore()

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
            <SwappableIcon icon={DarkModeIcon} altIcon={LightModeIcon} altIconActive={$darkTheme} rotate>
                <input class="theme-controller" type="checkbox" value="dark" />
            </SwappableIcon>
        </span>
    </button>

    {#if $isSafari}
        <details class="dropdown dropdown-end dropdown-bottom flex items-center">
            <summary class="h-6 w-6 cursor-pointer">
                <ExpandIcon />
            </summary>
            <ThemeSelectorDropdown {handleSelectTheme} />
        </details>
    {:else}
        <div class="dropdown dropdown-end dropdown-bottom flex items-center">
            <button class="h-6 w-6">
                <ExpandIcon />
            </button>
            <ThemeSelectorDropdown {handleSelectTheme} />
        </div>
    {/if}
</div>
