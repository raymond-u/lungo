<script lang="ts">
    import { FormBuilder, HeroFrame } from "$lib/components"
    import { SettingsIcon } from "$lib/icons"
</script>

<HeroFrame wrapped>
    <span class="text-balance text-center text-4xl">Manage account</span>
    <span class="mb-6 h-12 w-12">
        <SettingsIcon />
    </span>
    <FormBuilder />
</HeroFrame>
