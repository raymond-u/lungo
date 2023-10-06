import { createKetoClient, createKratosClient } from "$lib/server/api"
import { type App, EDependency, EIcon, type Fetch, type User } from "$lib/types"

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
    //         break
    //     default:
    //         return {
    //             apps: getAllowedApps(),
    //             logoutToken: undefined,
    //             userInfo: undefined,
    //         }
    // }
    //
    // const response2 = await client.GET("/self-service/logout/browser", { params: {} })
    //
    // switch (response2.response.status) {
    //     case 200:
    //         break
    //     default:
    //         return {
    //             apps: getAllowedApps(),
    //             logoutToken: undefined,
    //             userInfo: undefined,
    //         }
    // }
    //
    // const client2 = createKetoClient(fetch)
    // const response3 = await client2.GET("/relation-tuples", {
    //     params: {
    //         query: {
    //             namespace: "app",
    //             relation: "access",
    //             subject_id: (response.data!.identity as User).traits!.username,
    //         },
    //     },
    // })
    //
    // switch (response3.response.status) {
    //     case 200:
    //         return {
    //             apps: getAllowedApps(response3.data?.relation_tuples?.map((tuple) => tuple.object)),
    //             logoutToken: response2.data!.logout_token,
    //             userInfo: response.data!.identity.traits,
    //         }
    //     default:
    //         return {
    //             apps: getAllowedApps(),
    //             logoutToken: undefined,
    //             userInfo: undefined,
    //         }
    // }

    return {
        apps: getAllowedApps(),
        logoutToken: "abc123",
        userInfo: {
            username: "test",
            email: "test@gmail.com",
            name: {
                first: "Test",
                last: "User",
            },
        },
    }
}
