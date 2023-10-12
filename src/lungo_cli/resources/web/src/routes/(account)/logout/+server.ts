import { type Cookies, redirect } from "@sveltejs/kit"
import { invalidate } from "$app/navigation"
import { createKratosClient } from "$lib/server/api"
import { EDependency } from "$lib/types/common"

export async function POST({ cookies, request }: { cookies: Cookies; request: Request }) {
    const data = await request.formData()

    const client = createKratosClient(cookies, fetch)
    await client.GET("/self-service/logout", {
        params: { query: { token: data.get("logoutToken") as string } },
    })

    await invalidate(EDependency.Session)
    throw redirect(302, "/")
}