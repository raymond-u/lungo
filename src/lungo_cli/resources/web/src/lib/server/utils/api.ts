import createClient from "openapi-fetch"
import { type Cookies } from "@sveltejs/kit"
import { KETO_API_BASE_URL, KRATOS_API_BASE_URL } from "$lib/server/constants"
import type { KetoPaths, KratosPaths } from "$lib/types"
import { wrapFetch } from "$lib/utils"

export const createKetoClient = (fetch: typeof global.fetch) => {
    return createClient<KetoPaths>({
        fetch: wrapFetch({
            fetch,
            baseUrl: KETO_API_BASE_URL,
            credentials: "include",
            headers: { Accept: "application/json" },
        }),
    })
}

export const createKratosClient = (cookies: Cookies, fetch: typeof global.fetch) => {
    return createClient<KratosPaths>({
        fetch: wrapFetch({
            fetch,
            baseUrl: KRATOS_API_BASE_URL,
            cookies,
            credentials: "include",
            headers: { Accept: "application/json" },
        }),
    })
}
