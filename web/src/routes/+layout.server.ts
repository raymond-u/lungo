import { createKratosClient } from "$lib/api"
import { type App, EDependency, EIcon, type Fetch } from "$lib/types"

function getAllowedApps(allowedApps: string[] | undefined = undefined): App[] {
    allowedApps = allowedApps ?? []
    const apps = []

    if ("Files" in allowedApps) {
        apps.push({ name: "Files", href: "/app/files", icon: EIcon.Folder })
    }
    if ("Terminal" in allowedApps) {
        apps.push({ name: "Terminal", href: "/app/terminal", icon: EIcon.Terminal })
    }
    if ("RStudio" in allowedApps) {
        apps.push({ name: "R Studio", href: "/app/r-studio", icon: EIcon.RStudio })
    }
    if ("Proxy" in allowedApps) {
        apps.push({ name: "Proxy", href: "/app/proxy", icon: EIcon.Proxy })
    }

    return apps
}

export async function load({ depends, fetch }: { depends: (...deps: string[]) => void; fetch: Fetch }) {
    depends(EDependency.Session)

    // const client = createKratosClient(fetch)
    // const response = await client.GET("/sessions/whoami", { params: {} })
    //
    // switch (response.response.status) {
    //     case 200:
    //         return {
    //             identity: response.data!.identity.traits,
    //             apps: getAllowedApps(response.data!.identity.metadata_public?.["allowed_apps"] as string[] | undefined),
    //         }
    //     default:
    //         return {
    //             identity: undefined,
    //             apps: getAllowedApps(),
    //         }
    // }

    return {
        identity: {
            username: "test",
            email: "test@gmail.com",
            name: {
                first: "Test",
                last: "User",
            },
        },
        apps: getAllowedApps(),
    }
}
