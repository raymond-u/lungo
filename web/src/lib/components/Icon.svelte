<script lang="ts">
    import {
        Close,
        FolderOutline,
        FolderSolid,
        Menu,
        ProxyOutline,
        ProxySolid,
        RStudioOutline,
        RStudioSolid,
        TerminalOutline,
        TerminalSolid,
    } from "$lib/icons"
    import { EIcon } from "$lib/types"

    export let icon: EIcon
    export let active = false
    export let flip = false
    export let rotate = false

    const icons = {
        [EIcon.Folder]: {
            normal: FolderOutline,
            active: FolderSolid,
        },
        [EIcon.Menu]: {
            normal: Menu,
            active: Close,
        },
        [EIcon.Proxy]: {
            normal: ProxyOutline,
            active: ProxySolid,
        },
        [EIcon.RStudio]: {
            normal: RStudioOutline,
            active: RStudioSolid,
        },
        [EIcon.Terminal]: {
            normal: TerminalOutline,
            active: TerminalSolid,
        },
    }
</script>

<span class="swap" class:swap-active={active} class:swap-flip={flip} class:swap-rotate={rotate}>
    <svelte:component this={icons[icon].normal} class="swap-off fill-base-content" />
    <svelte:component this={icons[icon].active} class="swap-on fill-base-content" />
</span>
