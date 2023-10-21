import type { App } from "$lib/types"

export async function load({ parent, url }: { parent: () => Promise<{ apps: App[] }>; url: URL }) {
    const pathBase = url.pathname.match("^/app/[^/]+")

    if (!pathBase) {
        return {
            title: "",
        }
    }

    const { apps } = await parent()

    return {
        title: apps.find((app) => app.href === pathBase[0])?.name ?? "",
    }
}
