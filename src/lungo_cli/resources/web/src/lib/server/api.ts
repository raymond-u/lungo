import createClient from "openapi-fetch"
import parser from "set-cookie-parser"
import { type Cookies, error } from "@sveltejs/kit"
import { KETO_API_BASE_URL, KRATOS_API_BASE_URL } from "$lib/server/constants"
import type { KetoPaths, KratosPaths } from "$lib/types"

function wrapFetch(fetch: typeof global.fetch, cookies?: Cookies): typeof global.fetch {
    return async (input, init?) => {
        try {
            if (cookies && cookies.getAll().length > 0) {
                init ??= {}
                init.headers = new Headers(init.headers)
                init.headers.set(
                    "Cookie",
                    cookies
                        .getAll()
                        .map(({ name, value }) => `${name}=${value}`)
                        .join("; ")
                )
            }

            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            const response = await fetch(input, init)

            if (cookies) {
                for (const cookie of parser.parse(response.headers.getSetCookie())) {
                    cookies.set(cookie.name, cookie.value, {
                        path: "/",
                        expires: cookie.expires,
                        maxAge: cookie.maxAge,
                    })
                }
            }

            return response
        } catch (e) {
            throw error(500, "Failed to connect to server.")
        }
    }
}

export const createKetoClient = (fetch: typeof global.fetch) => {
    return createClient<KetoPaths>({
        baseUrl: KETO_API_BASE_URL,
        fetch: wrapFetch(fetch),
        credentials: "include",
        headers: { Accept: "application/json" },
    })
}

export const createKratosClient = (cookies: Cookies, fetch: typeof global.fetch) => {
    return createClient<KratosPaths>({
        baseUrl: KRATOS_API_BASE_URL,
        fetch: wrapFetch(fetch, cookies),
        credentials: "include",
        headers: { Accept: "application/json" },
    })
}
