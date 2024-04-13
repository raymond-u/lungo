import { createKratosClient } from "$lib/server/utils"

export async function POST({ cookies, fetch, request }) {
    const data = await request.formData()

    const client = createKratosClient(cookies, fetch)
    await client.GET("/self-service/logout", {
        params: { query: { token: data.get("logoutToken") as string } },
    })

    return new Response()
}
