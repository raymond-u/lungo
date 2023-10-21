<!--suppress ReservedWordAsName -->
<script lang="ts">
    let classString = ""
    export { classString as class }
</script>

<svg
    class="fill-base-content {classString}"
    height="100%"
    style="fill-rule:evenodd; clip-rule:evenodd; stroke-linejoin:round; stroke-miterlimit:2"
    viewBox="0 0 24 24"
    width="100%"
    xml:space="preserve"
    xmlns="http://www.w3.org/2000/svg"
>
    <slot />
</svg>
