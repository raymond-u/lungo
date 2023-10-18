import type { Cookies } from "@sveltejs/kit"
import * as cheerio from "cheerio"
import type { User } from "$lib/types"
// import { asSearchParams } from "$lib/utils"
import { wrapFetch } from "$lib/server/api"
import { error } from "@sveltejs/kit"

export async function load({
    cookies,
    fetch,
    parent,
}: {
    cookies: Cookies
    fetch: typeof global.fetch
    parent: () => Promise<{ userInfo: User | undefined }>
}) {
    const wrappedFetch = wrapFetch(fetch, cookies)

    try {
        const response = await wrappedFetch("/app/rstudio/auth-sign-in?iframe=1", { redirect: "manual" })

        // If the user is already logged in, return
        if (response.status === 302) {
            return {
                title: "R Studio",
            }
        }

        const $ = cheerio.load(await response.text())
        const key = $("meta[name=public-key-url]").attr("content")!

        // const html = new DOMParser().parseFromString(await response.text(), "text/html")
        // const key = html.getElementsByName("public-key-url")[0].getAttribute("content")

        const { userInfo } = await parent()

        const response2 = await wrappedFetch("/app/rstudio/js/encrypt.min.js?iframe=1")
        const text = await response2.text()
        const encrypt = new Function(
            "payload",
            "exp",
            "mod",
            `"use strict"; ${text.replace("window.encrypt", "var encrypt")}; return encrypt(payload, exp, mod);`
        ) as (payload: string, exp: string, mod: string) => string

        const username = userInfo?.traits?.username ?? "anonymous"
        const password = "passwd"
        const payload = `${username}\n${password}`

        const response3 = await wrappedFetch(`/app/rstudio/${key}?iframe=1`)
        const text2 = await response3.text()
        const [exp, mod] = text2.split(":", 2)

        const csrf = $("form[name=realform] > input:eq(1)")
        // ;(html.getElementById("clientPath") as HTMLInputElement).value = "/app/rstudio/auth-sign-in"
        // ;(html.getElementById("package") as HTMLInputElement).value = encrypt(payload, exp, mod)
        // ;(html.getElementById("persist") as HTMLInputElement).value = "0"

        await wrappedFetch("/app/rstudio/auth-do-sign-in?iframe=1", {
            method: "POST",
            redirect: "manual",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                persist: "0",
                [csrf.attr("name")!]: csrf.attr("value")!,
                appUri: "/",
                clientPath: "/app/rstudio/auth-sign-in",
                v: encrypt(payload, exp, mod),
            }),
            // body: asSearchParams(html.getElementsByName("realform")[0] as HTMLFormElement),
        })
    } catch (e) {
        console.log("####################")
        console.log(e)
        console.log(JSON.stringify(e))
        console.log("####################")
        throw error(500, "Failed to connect to server.")
    }

    return {
        title: "R Studio",
    }
}
