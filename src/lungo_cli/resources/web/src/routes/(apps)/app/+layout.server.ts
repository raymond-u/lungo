import { getAllApps } from "$lib/server/utils"

export async function load({ url }) {
    const pathBase = url.pathname.match("^/app/[^/]+")

    if (!pathBase) {
        return {
            title: "Unknown",
        }
    }

    for (const app of getAllApps()) {
        if (app.href === pathBase[0]) {
            return {
                title: app.descriptiveName,
            }
        }
    }

    return {
        title: "Unknown",
    }
}
