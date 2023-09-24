import { redirect } from "@sveltejs/kit"

// noinspection JSUnusedGlobalSymbols
export function load() {
    throw redirect(301, "/")
}
