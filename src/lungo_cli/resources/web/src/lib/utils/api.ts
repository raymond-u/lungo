import { type Cookies, error } from "@sveltejs/kit"
import parser from "set-cookie-parser"
import { concatenateUrl } from "$lib/utils"

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
    baseUrl?: string | URL
    cookies?: Cookies
    cookiePath?: string
    credentials?: RequestCredentials
    headers?: HeadersInit
    ensureOk?: boolean
}): typeof global.fetch {
    return async (input, init?) => {
        let response: Response

        try {
            init ??= {}

            if (input instanceof Request) {
                init.headers = new Headers(init.headers || input.headers)
            } else {
                init.headers = new Headers(init.headers)
            }

            if (baseUrl) {
                if (typeof input === "string" || input instanceof URL) {
                    input = concatenateUrl(input, baseUrl)
                } else if (input instanceof Request) {
                    input = new Request(concatenateUrl(input.url, baseUrl), input)
                }
            }

            if (cookies && cookies.getAll().length > 0) {
                init.headers.set(
                    "Cookie",
                    cookies
                        .getAll()
                        .map(({ name, value }) => `${name}=${value}`)
                        .join("; ")
                )
            }

            if (credentials) {
                init.credentials = credentials
            }

            if (headers) {
                for (const [key, value] of Object.entries(headers)) {
                    init.headers.set(key, value)
                }
            }

            if (input instanceof Request) {
                response = await fetch(new Request(input, init))
            } else {
                response = await fetch(input, init)
            }

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
            error(500)
        }

        if (ensureOk && response.status >= 400 && response.status < 600) {
            error(response.status)
        }

        return response
    }
}
