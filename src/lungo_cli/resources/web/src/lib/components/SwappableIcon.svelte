<!--suppress ReservedWordAsName -->
<script lang="ts">
    import type { ComponentType } from "svelte"

    let classString = ""
    export { classString as class }

    export let icon: ComponentType
    export let altIcon: ComponentType
    export let altIconActive = false
    export let flip = false
    export let rotate = false
</script>

<span class="swap" class:swap-active={altIconActive} class:swap-flip={flip} class:swap-rotate={rotate}>
    <svelte:component this={icon} class="swap-off {classString}" />
    <svelte:component this={altIcon} class="swap-on {classString}" />
    <slot />
</span>
