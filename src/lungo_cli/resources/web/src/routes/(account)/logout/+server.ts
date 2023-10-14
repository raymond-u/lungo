import type { Cookies } from "@sveltejs/kit"
import { createKratosClient } from "$lib/server/api"

export async function POST({ cookies, request }: { cookies: Cookies; request: Request }) {
    const data = await request.formData()

    const client = createKratosClient(cookies, fetch)
    await client.GET("/self-service/logout", {
        params: { query: { token: data.get("logoutToken") as string } },
    })
}
