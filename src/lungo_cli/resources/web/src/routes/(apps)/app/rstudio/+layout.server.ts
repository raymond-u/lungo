import { load as loadHtmlString } from "cheerio"
import type { Cookies } from "@sveltejs/kit"
import { wrapFetch } from "$lib/server/api"
import { RSTUDIO_BASE_URL } from "$lib/server/constants"
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
        return {
            title: "R Studio",
        }
    }

    const $ = loadHtmlString(await response.text())
    const key = $("meta[name=public-key-url]").attr("content")!

    const response2 = await wrappedFetch(`/${key}`)
    const text2 = await response2.text()
    const [exp, mod] = text2.split(":", 2)

    const response3 = await wrappedFetch("/js/encrypt.min.js")
    const text = await response3.text()
    const encrypt = new Function(
        "payload",
        "exp",
        "mod",
        `"use strict";
        const navigator = { appName: "Netscape", appVersion: "5.0" };
        ${text.replace("window.encrypt", "var encrypt")};
        return encrypt(payload, exp, mod);`
    ) as (payload: string, exp: string, mod: string) => string

    const { userInfo } = await parent()

    const username = userInfo?.username ?? "anonymous"
    const password = "passwd"
    const payload = `${username}\n${password}`

    const csrf = $("form[name=realform] > input:eq(1)")

    for (;;) {
        const response4 = await wrappedFetch("/auth-do-sign-in", {
            method: "POST",
            redirect: "manual",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                // "X-RStudio-Root-Path": "/app/rstudio",
                // "X-Forwarded-Proto": "https",
                // "X-Forwarded-Host": "172.16.39.102",
            },
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

    return {
        title: "R Studio",
    }
}
