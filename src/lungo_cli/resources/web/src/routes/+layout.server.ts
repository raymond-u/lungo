import type { Cookies } from "@sveltejs/kit"
import { createKetoClient, createKratosClient } from "$lib/server/api"
import { getAllApps } from "$lib/server/utils"
import type { AppInfo, User } from "$lib/types"

async function getAllowedApps(fetch: typeof global.fetch, username?: string): Promise<AppInfo[]> {
    const client = createKetoClient(fetch)
    const apps = []

    for (const app of getAllApps()) {
        const response = await client.GET("/relation-tuples/check", {
            params: {
                query: {
                    namespace: "app",
                    object: app.name,
                    relation: "access",
                    subject_id: username ?? "anonymous",
                },
            },
        })

        switch (response.response.status) {
            case 200:
                apps.push(app)
                break
        }
    }

    return apps
}

export async function load({ cookies, fetch, url }: { cookies: Cookies; fetch: typeof global.fetch; url: URL }) {
    const title = url.pathname.split("/").pop() || "home"

    const client = createKratosClient(cookies, fetch)
    const response = await client.GET("/sessions/whoami", { params: {} })

    switch (response.response.status) {
        case 200:
            break
        default:
            return {
                apps: await getAllowedApps(fetch),
                logoutToken: undefined,
                title,
                userInfo: undefined,
            }
    }

    const response2 = await client.GET("/self-service/logout/browser", { params: {} })

    switch (response2.response.status) {
        case 200:
            return {
                apps: await getAllowedApps(fetch, (response.data!.identity as User).traits!.username),
                logoutToken: response2.data!.logout_token,
                title,
                userInfo: (response.data!.identity as User).traits,
            }
        default:
            return {
                apps: await getAllowedApps(fetch),
                logoutToken: undefined,
                title,
                userInfo: undefined,
            }
    }

    // return {
    //     apps: [],
    //     logoutToken: "test123",
    //     title,
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
