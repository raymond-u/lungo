<script lang="ts">
    import { FormBuilder, HeroFrame } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { AccountIcon } from "$lib/icons"
</script>

<HeroFrame wrapped>
    <span class="text-balance text-center text-4xl">Welcome to {SITE_TITLE}</span>
    <span class="mb-6 h-12 w-12">
        <AccountIcon />
    </span>
    <FormBuilder primaryGroup="password" validationFreeButtons={["resend"]}>
        <span class="inline-flex">
            <a class="link text-sm" href="/recover">Forgot password?</a>
        </span>
    </FormBuilder>
</HeroFrame>
