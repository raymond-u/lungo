import { EApp } from "$lib/server/types"
import { createApp } from "$lib/server/utils"

export async function load({ url }: { url: URL }) {
    const pathBase = url.pathname.match("^/app/[^/]+")

    if (!pathBase) {
        return {
            title: "",
        }
    }

    for (const app in EApp) {
        const { href, name } = createApp(EApp[app as keyof typeof EApp])

        if (href === pathBase[0]) {
            return {
                title: name,
            }
        }
    }

    return {
        title: "",
    }
}
