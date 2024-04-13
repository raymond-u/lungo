import { load as loadHtmlString } from "cheerio"
import { JUPYTERHUB_BASE_URL, JUPYTERHUB_PASSWORD } from "$lib/plugins/jupyterhub/server/constants.server"
import { wrapFetch } from "$lib/utils"

export async function load({ cookies, fetch, parent }) {
    const wrappedFetch = wrapFetch({
        fetch,
        baseUrl: JUPYTERHUB_BASE_URL,
        cookies,
        cookiePath: "/app/jupyterhub",
        credentials: "include",
        ensureOk: true,
    })

    const response = await wrappedFetch("/app/jupyterhub/hub/login", { redirect: "manual" })

    // If the user is already logged in, return
    if (response.status == 302) {
        return
    }

    const $ = loadHtmlString(await response.text())
    const csrf = $("#login-main input[name=_xsrf]").attr("value")!

    const { userInfo } = await parent()
    const username = userInfo?.username ?? "anonymous"

    await wrappedFetch("/app/jupyterhub/hub/login", {
        method: "POST",
        redirect: "manual",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
            _xsrf: csrf,
            username,
            password: JUPYTERHUB_PASSWORD,
        }),
    })
}
