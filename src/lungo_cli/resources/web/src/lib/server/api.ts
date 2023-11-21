import createClient from "openapi-fetch"
import parser from "set-cookie-parser"
import { type Cookies, error } from "@sveltejs/kit"
import { KETO_API_BASE_URL, KRATOS_API_BASE_URL } from "$lib/server/constants"
import type { KetoPaths, KratosPaths } from "$lib/types"

export function wrapFetch({
    fetch,
    baseUrl,
    cookies,
    cookiePath,
    credentials,
    headers,
    ensureOk,
}: {
    fetch: typeof global.fetch
    baseUrl?: string
    cookies?: Cookies
    cookiePath?: string
    credentials?: RequestCredentials
    headers?: HeadersInit
    ensureOk?: boolean
}): typeof global.fetch {
    return async (input, init?) => {
        let response: Response

        try {
            if (baseUrl) {
                if (typeof input === "string") {
                    if (input.match("https?://")) {
                        const url = new URL(input)
                        input = new URL(url.pathname + url.search + url.hash, baseUrl)
                    } else {
                        input = new URL(input, baseUrl)
                    }
                } else if (input instanceof URL) {
                    input = new URL(input.pathname + input.search + input.hash, baseUrl)
                } else if (input instanceof Request) {
                    const url = new URL(input.url)
                    input = new Request(new URL(url.pathname + url.search + url.hash, baseUrl), input)
                }
            }

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

            if (credentials) {
                init ??= {}
                init.credentials = credentials
            }

            if (headers) {
                init ??= {}
                init.headers = new Headers(init.headers)
                for (const [key, value] of Object.entries(headers)) {
                    init.headers.set(key, value)
                }
            }

            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            response = await fetch(input, init)

            if (cookies) {
                for (const cookie of parser.parse(response.headers.getSetCookie(), { decodeValues: false })) {
                    cookies.set(cookie.name, cookie.value, {
                        encode: (value) => value,
                        path: cookiePath || "/",
                        expires: cookie.expires,
                        maxAge: cookie.maxAge,
                    })
                }
            }
        } catch (e) {
            throw error(500)
        }

        if (ensureOk && !(response.status >= 200 && response.status < 400)) {
            throw error(response.status)
        }

        return response
    }
}

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
