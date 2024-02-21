import { redirect } from "@sveltejs/kit"

// noinspection JSUnusedGlobalSymbols
export function load() {
    redirect(301, "/")
}
