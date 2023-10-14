import type { Cookies } from "@sveltejs/kit"
import { createKetoClient, createKratosClient } from "$lib/server/api"
import { EApp } from "$lib/server/types"
import { type App, EIcon, type User } from "$lib/types"

async function getAllowedApps(fetch: typeof global.fetch, username?: string): Promise<App[]> {
    const client = createKetoClient(fetch)
    const allowedApps = []
    const apps = []

    for (const app of Object.values(EApp)) {
        const response = await client.GET("/relation-tuples/check", {
            params: {
                query: {
                    namespace: "app",
                    object: app,
                    relation: "access",
                    subject_id: username ?? "anonymous",
                },
            },
        })

        switch (response.response.status) {
            case 200:
                allowedApps.push(app)
                break
            default:
                break
        }
    }

    console.log("@@@@@@@@@")
    console.log(JSON.stringify(allowedApps))
    console.log("@@@@@@@@@")
    console.log(EApp.FileBrowser)
    console.log("@@@@@@@@@")
    console.log(EApp.RStudio)
    console.log("@@@@@@@@@")

    if (EApp.FileBrowser in allowedApps) {
        apps.push({ name: "Files", href: "/app/files", icon: EIcon.Folder })
    }
    // if ("terminal" in allowedApps) {
    //     apps.push({ name: "Terminal", href: "/app/terminal", icon: EIcon.Terminal })
    // }
    if (EApp.RStudio in allowedApps) {
        apps.push({ name: "R Studio", href: "/app/r-studio", icon: EIcon.RStudio })
    }
    // if ("proxy" in allowedApps) {
    //     apps.push({ name: "Proxy", href: "/app/proxy", icon: EIcon.Proxy })
    // }

    return apps
}

export async function load({ cookies, fetch }: { cookies: Cookies; fetch: typeof global.fetch }) {
    const client = createKratosClient(cookies, fetch)
    const response = await client.GET("/sessions/whoami", { params: {} })

    switch (response.response.status) {
        case 200:
            break
        default:
            return {
                apps: await getAllowedApps(fetch),
                logoutToken: undefined,
                userInfo: undefined,
            }
    }

    const response2 = await client.GET("/self-service/logout/browser", { params: {} })

    switch (response2.response.status) {
        case 200:
            return {
                apps: await getAllowedApps(fetch, (response.data!.identity as User).traits!.username),
                logoutToken: response2.data!.logout_token,
                userInfo: (response.data!.identity as User).traits,
            }
        default:
            return {
                apps: await getAllowedApps(fetch),
                logoutToken: undefined,
                userInfo: undefined,
            }
    }

    // return {
    //     apps: [],
    //     logoutToken: "abc123",
    //     userInfo: {
    //         username: "test",
    //         email: "testuser12345@gmail.com",
    //         name: {
    //             first: "Test",
    //             last: "User",
    //         },
    //     },
    // }
}
