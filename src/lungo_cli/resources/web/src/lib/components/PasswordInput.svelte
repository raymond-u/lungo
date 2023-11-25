<script lang="ts">
    import { SwappableIcon } from "$lib/components"
    import { EIcon } from "$lib/types"

    export let name = ""
    export let value = ""
    export let disabled = false
    export let required = false
    export let autocomplete = "off"
    export let placeholder = ""

    const handleClick = () => {
        visible = !visible
    }

    let visible = false
</script>

<span class="relative inline-flex">
    <input
        class="input flex-1 pr-12"
        {name}
        type={visible ? "text" : "password"}
        {value}
        {disabled}
        {required}
        {autocomplete}
        {placeholder}
    />
    <button class="absolute right-3 top-3 h-6 w-6" type="button" on:click={handleClick}>
        <SwappableIcon active={visible} icon={EIcon.Visibility} />
    </button>
</span>
