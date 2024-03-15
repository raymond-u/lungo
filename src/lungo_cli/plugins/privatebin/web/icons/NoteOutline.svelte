<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import type { ComponentProps } from "svelte"
    import BaseIcon from "$lib/icons/BaseIcon.svelte"

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    type $$Props = ComponentProps<BaseIcon>
</script>

<BaseIcon {...$$restProps}>
    <path
        d="M5,19L14,19L14,14L19,14L19,5L5,5L5,19ZM5,21C4.45,21 3.979,20.804 3.588,20.413C3.196,20.021 3,19.55 3,19L3,5C3,4.45 3.196,3.979 3.588,3.587C3.979,3.196 4.45,3 5,3L19,3C19.55,3 20.021,3.196 20.413,3.587C20.804,3.979 21,4.45 21,5L21,15L15,21L5,21ZM7,14L7,12L12,12L12,14L7,14ZM7,10L7,8L17,8L17,10L7,10ZM5,19L5,5L5,19Z"
        style="fill-rule:nonzero"
    />
</BaseIcon>
