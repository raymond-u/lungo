import { getAllApps } from "$lib/server/utils"

export async function load({ url }: { url: URL }) {
    const pathBase = url.pathname.match("^/app/[^/]+")

    if (!pathBase) {
        return {
            title: "",
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
        title: "",
    }
}
