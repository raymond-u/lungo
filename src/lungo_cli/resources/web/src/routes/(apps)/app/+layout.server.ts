import { getAllApps, getAppInfo } from "$lib/server/utils"

export async function load({ url }: { url: URL }) {
    const pathBase = url.pathname.match("^/app/[^/]+")

    if (!pathBase) {
        return {
            title: "",
        }
    }

    for (const app of await getAllApps()) {
        const { descriptiveName, href } = await getAppInfo(app)

        if (href === pathBase[0]) {
            return {
                title: descriptiveName,
            }
        }
    }

    return {
        title: "",
    }
}
