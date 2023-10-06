import createClient from "openapi-fetch"
import { error } from "@sveltejs/kit"
import { KETO_API_BASEURL, KRATOS_API_BASEURL } from "$env/static/private"
import type { Fetch, KetoPaths, KratosPaths } from "$lib/types"

function wrapFetch(fetch: Fetch): Fetch {
    if (!fetch) {
        return undefined
    }

    return async (input: RequestInfo | URL, init?: RequestInit | undefined) => {
        try {
            return await fetch(input, init)
        } catch (e) {
            throw error(500, "Failed to connect to server.")
        }
    }
}

export const createKetoClient = (fetch: Fetch) => {
    return createClient<KetoPaths>({
        baseUrl: KETO_API_BASEURL,
        fetch: wrapFetch(fetch),
        credentials: "include",
        headers: { Accept: "application/json" },
    })
}

export const createKratosClient = (fetch: Fetch) => {
    return createClient<KratosPaths>({
        baseUrl: KRATOS_API_BASEURL,
        fetch: wrapFetch(fetch),
        credentials: "include",
        headers: { Accept: "application/json" },
    })
}
