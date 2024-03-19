<script lang="ts">
    import { FormBuilder, HeroFrame } from "$lib/components"
    import { ResetIcon } from "$lib/icons"
</script>

<HeroFrame wrapped>
    <span class="text-balance text-center text-4xl">Recover your account</span>
    <span class="mb-6 h-12 w-12">
        <ResetIcon />
    </span>
    <FormBuilder validationFreeButtons={["email"]} />
</HeroFrame>
