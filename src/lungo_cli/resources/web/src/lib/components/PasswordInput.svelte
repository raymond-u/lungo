<script lang="ts">
    import { SwapIcon } from "$lib/components"
    import { EIcon } from "$lib/types"
    import { useStore } from "$lib/utils"

    export let name = ""
    export let value = ""
    export let disabled = false
    export let required = false
    export let autocomplete = "off"
    export let placeholder = ""

    const { darkTheme } = useStore()

    const handleClick = () => {
        visible = !visible
    }

    let visible = false
</script>

<span class="relative inline-flex">
    <input
        class="input flex-1 pr-12"
        class:bg-base-200={!$darkTheme}
        {name}
        type={visible ? "text" : "password"}
        {value}
        {disabled}
        {required}
        {autocomplete}
        {placeholder}
    />
    <button class="absolute right-3 top-3 h-6 w-6" type="button" on:click={handleClick}>
        <SwapIcon active={visible} icon={EIcon.Visibility} />
    </button>
</span>
