<script lang="ts">
    import { FormBuilder } from "$lib/components"
    import { SITE_TITLE } from "$lib/constants"
    import { AccountIcon } from "$lib/icons"
</script>

<div class="flex h-full w-full flex-col items-center overflow-y-auto">
    <div class="flex w-full flex-1 items-center justify-center py-16">
        <div
            class="flex max-w-md flex-1 flex-col items-center justify-center gap-4 rounded-2xl bg-base-200 px-12 py-16"
        >
            <span class="text-center text-4xl">Welcome to {SITE_TITLE}</span>
            <span class="mb-6 h-12 w-12">
                <AccountIcon />
            </span>
            <FormBuilder>
                <span class="inline-flex">
                    <a class="link text-sm" href="/recover">Forgot password?</a>
                </span>
            </FormBuilder>
        </div>
    </div>
</div>
