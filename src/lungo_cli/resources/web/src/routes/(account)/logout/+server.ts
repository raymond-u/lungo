import { createKratosClient } from "$lib/server/utils"
import { getCookieHeader } from "$lib/utils"

export async function POST({ cookies, fetch, request }) {
    const data = await request.formData()

    const client = createKratosClient(getCookieHeader(request), cookies, fetch)
    await client.GET("/self-service/logout", {
        params: { query: { token: data.get("logoutToken") as string } },
    })

    return new Response()
}
