<script lang="ts">
    import {
        CloseIcon,
        DarkModeIcon,
        FolderOutlineIcon,
        FolderSolidIcon,
        LightModeIcon,
        MenuIcon,
        PastebinOutlineIcon,
        PastebinSolidIcon,
        ProxyOutlineIcon,
        ProxySolidIcon,
        RStudioOutlineIcon,
        RStudioSolidIcon,
        TerminalOutlineIcon,
        TerminalSolidIcon,
        VisibilityOffIcon,
        VisibilityOnIcon,
    } from "$lib/icons"
    import { EIcon } from "$lib/types"

    export let icon: EIcon
    export let active = false
    export let flip = false
    export let rotate = false

    const icons = {
        [EIcon.Folder]: {
            normal: FolderOutlineIcon,
            active: FolderSolidIcon,
        },
        [EIcon.Menu]: {
            normal: MenuIcon,
            active: CloseIcon,
        },
        [EIcon.Pastebin]: {
            normal: PastebinOutlineIcon,
            active: PastebinSolidIcon,
        },
        [EIcon.Proxy]: {
            normal: ProxyOutlineIcon,
            active: ProxySolidIcon,
        },
        [EIcon.RStudio]: {
            normal: RStudioOutlineIcon,
            active: RStudioSolidIcon,
        },
        [EIcon.Terminal]: {
            normal: TerminalOutlineIcon,
            active: TerminalSolidIcon,
        },
        [EIcon.Theme]: {
            normal: DarkModeIcon,
            active: LightModeIcon,
        },
        [EIcon.Visibility]: {
            normal: VisibilityOnIcon,
            active: VisibilityOffIcon,
        },
    }
</script>

<span class="swap" class:swap-active={active} class:swap-flip={flip} class:swap-rotate={rotate}>
    <svelte:component this={icons[icon].normal} class="swap-off" />
    <svelte:component this={icons[icon].active} class="swap-on" />
</span>
