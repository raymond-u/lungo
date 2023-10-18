import { load as loadHtmlString } from "cheerio"
import { type Cookies, error } from "@sveltejs/kit"
import { wrapFetch } from "$lib/server/api"
import { RSTUDIO_BASE_URL } from "$lib/server/constants"
import type { User } from "$lib/types"
// import { asSearchParams } from "$lib/utils"

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
        console.log("##### get 1 #####")

        const response = await wrappedFetch(`${RSTUDIO_BASE_URL}auth-sign-in`, { redirect: "manual" })

        // If the user is already logged in, return
        if (response.status === 302) {
            return {
                title: "R Studio",
            }
        }

        console.log("##### get 2 #####")

        const $ = loadHtmlString(await response.text())
        const key = $("meta[name=public-key-url]").attr("content")!

        console.log("##### get 3 #####")

        // const html = new DOMParser().parseFromString(await response.text(), "text/html")
        // const key = html.getElementsByName("public-key-url")[0].getAttribute("content")

        const { userInfo } = await parent()

        console.log("##### get 4 #####")

        const response2 = await wrappedFetch(`${RSTUDIO_BASE_URL}js/encrypt.min.js`)
        const text = await response2.text()
        const encrypt = new Function(
            "payload",
            "exp",
            "mod",
            `"use strict"; ${text.replace("window.encrypt", "var encrypt")}; return encrypt(payload, exp, mod);`
        ) as (payload: string, exp: string, mod: string) => string

        console.log("##### get 5 #####")

        const username = userInfo?.traits?.username ?? "anonymous"
        const password = "passwd"
        const payload = `${username}\n${password}`

        const response3 = await wrappedFetch(`${RSTUDIO_BASE_URL}${key}`)
        const text2 = await response3.text()
        const [exp, mod] = text2.split(":", 2)

        console.log("##### get 6 #####")

        const csrf = $("form[name=realform] > input:eq(1)")
        // ;(html.getElementById("clientPath") as HTMLInputElement).value = "/app/rstudio/auth-sign-in"
        // ;(html.getElementById("package") as HTMLInputElement).value = encrypt(payload, exp, mod)
        // ;(html.getElementById("persist") as HTMLInputElement).value = "0"

        await wrappedFetch(`${RSTUDIO_BASE_URL}auth-do-sign-in`, {
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

        console.log("##### get 7 #####")
    } catch (e) {
        console.log("####################")
        console.log(e)
        console.log(JSON.stringify(e))
        console.log("####################")
        throw error(500, "Failed to connect to server.")
    }

    console.log("##### get 8 #####")

    return {
        title: "R Studio",
    }
}
