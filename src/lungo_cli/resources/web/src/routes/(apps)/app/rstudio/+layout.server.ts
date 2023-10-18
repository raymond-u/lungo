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

    const testFetch = wrapFetch({
        fetch,
        baseUrl: "https://httpbin.org/",
        cookies,
        credentials: "include",
        ensureOk: true,
    })

    console.log("##### get 1 #####")

    const response = await wrappedFetch("/auth-sign-in", {
        redirect: "manual",
    })

    // If the user is already logged in, return
    if (response.status == 302) {
        return {
            title: "R Studio",
        }
    }

    console.log("##### get 2 #####")

    const $ = loadHtmlString(await response.text())
    const key = $("meta[name=public-key-url]").attr("content")!

    console.log("##### get 3 #####")

    const response2 = await wrappedFetch(`/${key}`)
    const text2 = await response2.text()
    const [exp, mod] = text2.split(":", 2)

    console.log("##### get 4 #####")

    // const html = new DOMParser().parseFromString(await response.text(), "text/html")
    // const key = html.getElementsByName("public-key-url")[0].getAttribute("content")

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

    console.log("##### get 5 #####")

    const { userInfo } = await parent()

    const username = userInfo?.username ?? "anonymous"
    const password = "passwd"
    const payload = `${username}\n${password}`

    console.log(`##### get ${payload} #####`)

    const csrf = $("form[name=realform] > input:eq(1)")
    // ;(html.getElementById("clientPath") as HTMLInputElement).value = "/app/rstudio/auth-sign-in"
    // ;(html.getElementById("package") as HTMLInputElement).value = encrypt(payload, exp, mod)
    // ;(html.getElementById("persist") as HTMLInputElement).value = "0"

    const response4 = await wrappedFetch("/auth-do-sign-in", {
        method: "POST",
        redirect: "manual",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-RStudio-Root-Path": "/app/rstudio",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Host": "172.16.39.102",
        },
        body: new URLSearchParams({
            persist: "0",
            [csrf.attr("name")!]: csrf.attr("value")!,
            appUri: "/",
            clientPath: "/app/rstudio/auth-sign-in",
            v: encrypt(payload, exp, mod),
        }).toString(),
        // body: asSearchParams(html.getElementsByName("realform")[0] as HTMLFormElement),
    })

    console.log(`##### get ${await response4.text()} #####`)

    const response0 = await testFetch("/post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            a: new URLSearchParams({
                persist: "0",
                [csrf.attr("name")!]: csrf.attr("value")!,
                appUri: "/",
                clientPath: "/app/rstudio/auth-sign-in",
                v: encrypt(payload, exp, mod),
            }).toString(),
        }),
        // body: asSearchParams(html.getElementsByName("realform")[0] as HTMLFormElement),
    })

    console.log(`##### get ${JSON.stringify(await response0.json())} #####`)

    return {
        title: "R Studio",
    }
}
