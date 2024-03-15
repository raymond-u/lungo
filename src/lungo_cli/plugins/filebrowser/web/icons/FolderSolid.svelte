<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import type { ComponentProps } from "svelte"
    import BaseIcon from "$lib/icons/BaseIcon.svelte"

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    type $$Props = ComponentProps<BaseIcon>
</script>

<BaseIcon {...$$restProps}>
    <path
        d="M4,20C3.45,20 2.979,19.804 2.588,19.413C2.196,19.021 2,18.55 2,18L2,6C2,5.45 2.196,4.979 2.588,4.587C2.979,4.196 3.45,4 4,4L9.175,4C9.442,4 9.696,4.05 9.938,4.15C10.179,4.25 10.392,4.392 10.575,4.575L12,6L20,6C20.55,6 21.021,6.196 21.413,6.587C21.804,6.979 22,7.45 22,8L22,18C22,18.55 21.804,19.021 21.413,19.413C21.021,19.804 20.55,20 20,20L4,20Z"
        style="fill-rule:nonzero"
    />
</BaseIcon>
