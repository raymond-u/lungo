<script lang="ts">
    import { page } from "$app/stores"
    import { safeClick } from "$lib/actions"
    import { LogoutIcon, SettingsIcon } from "$lib/icons"
    import { getNameInitials } from "$lib/utils"

    export let email: string
    export let firstName: string
    export let lastName: string

    const handleLogout = async () => {
        await fetch("/logout", {
            method: "POST",
            body: new URLSearchParams({ logoutToken: $page.data.logoutToken }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })

        location.reload()
    }
</script>

<ul class="menu dropdown-content z-20 mt-2 rounded-box bg-base-200 p-2 shadow">
    <li>
        <div class="pointer-events-none flex">
            <span
                class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-accent text-lg font-bold text-accent-content"
            >
                {getNameInitials(firstName, lastName)}
            </span>
            <div class="flex flex-col">
                <span class="text-base font-semibold">{firstName} {lastName}</span>
                <span>{email}</span>
            </div>
        </div>
    </li>
    <li><div class="divider menu-title pointer-events-none"></div></li>
    <li>
        <a href="/account">
            <span class="h-6 w-6">
                <SettingsIcon />
            </span>
            <span>Manage account</span>
        </a>
    </li>
    <li>
        <button use:safeClick={{ callback: handleLogout }}>
            <span class="h-6 w-6">
                <LogoutIcon />
            </span>
            <span>Log out</span>
        </button>
    </li>
</ul>
