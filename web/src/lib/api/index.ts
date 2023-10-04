import createClient from "openapi-fetch"
import { error } from "@sveltejs/kit"
import { KRATOS_API_BASEURL } from "$env/static/private"
import type { Fetch } from "$lib/types"
import type { paths as kratosPaths } from "./kratos"

export type { components as kratosComponents } from "./kratos"
export type { kratosPaths }

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

export const createKratosClient = (fetch: Fetch) => {
    return createClient<kratosPaths>({
        baseUrl: KRATOS_API_BASEURL,
        fetch: wrapFetch(fetch),
        credentials: "include",
        headers: { Accept: "application/json" },
    })
}
