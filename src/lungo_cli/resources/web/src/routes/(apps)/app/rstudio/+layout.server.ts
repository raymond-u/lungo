import { load as loadHtmlString } from "cheerio"
import type { Cookies } from "@sveltejs/kit"
import { wrapFetch } from "$lib/server/api"
import { RSTUDIO_BASE_URL, RSTUDIO_PASSWORD } from "$lib/server/constants"
import type { User } from "$lib/types"

export async function load({
    cookies,
    fetch,
    parent,
}: {
    cookies: Cookies
    fetch: typeof global.fetch
    parent: () => Promise<{ userInfo: User["traits"] | undefined }>
}) {
    const wrappedFetch = wrapFetch({
        fetch,
        baseUrl: RSTUDIO_BASE_URL,
        cookies,
        cookiePath: "/app/rstudio",
        credentials: "include",
        ensureOk: true,
    })

    const response = await wrappedFetch("/auth-sign-in", { redirect: "manual" })

    // If the user is already logged in, return
    if (response.status == 302) {
        return
    }

    const $ = loadHtmlString(await response.text())
    const key = $("meta[name=public-key-url]").attr("content")!

    const response2 = await wrappedFetch(`/${key}`)
    const [exp, mod] = (await response2.text()).split(":", 2)

    const response3 = await wrappedFetch("/js/encrypt.min.js")
    const script = await response3.text()

    const encrypt = new Function(
        "payload",
        "exp",
        "mod",
        `"use strict";
        const navigator = { appName: "Netscape", appVersion: "5.0" };
        ${script.replace("window.encrypt", "var encrypt")};
        return encrypt(payload, exp, mod);`
    ) as (payload: string, exp: string, mod: string) => string

    const { userInfo } = await parent()

    const username = userInfo?.username ?? "anonymous"
    const payload = `${username}\n${RSTUDIO_PASSWORD}`

    const csrf = $("form[name=realform] > input:eq(1)")

    for (;;) {
        const response4 = await wrappedFetch("/auth-do-sign-in", {
            method: "POST",
            redirect: "manual",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                persist: "0",
                [csrf.attr("name")!]: csrf.attr("value")!,
                appUri: "/",
                clientPath: "/auth-sign-in",
                v: encrypt(payload, exp, mod),
            }),
        })

        if (response4.headers.getSetCookie().length > 0) {
            break
        }
    }
}
