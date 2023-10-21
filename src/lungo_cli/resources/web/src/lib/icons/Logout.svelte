<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import type { ComponentProps } from "svelte"
    import BaseIcon from "./BaseIcon.svelte"

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    type $$Props = ComponentProps<BaseIcon>
</script>

<BaseIcon {...$$restProps}>
    <path
        d="M5,21C4.45,21 3.979,20.804 3.588,20.413C3.196,20.021 3,19.55 3,19L3,5C3,4.45 3.196,3.979 3.588,3.587C3.979,3.196 4.45,3 5,3L12,3L12,5L5,5L5,19L12,19L12,21L5,21ZM16,17L14.625,15.55L17.175,13L9,13L9,11L17.175,11L14.625,8.45L16,7L21,12L16,17Z"
        style="fill-rule:nonzero"
    />
</BaseIcon>
