import { load as loadHtmlString } from "cheerio"
import {
    JUPYTERHUB_BASE_URL,
    JUPYTERHUB_PASSWORD,
    JUPYTERHUB_WEB_PREFIX,
} from "$lib/plugins/jupyterhub/server/constants.server"
import { getCookieHeader, wrapFetch } from "$lib/utils"

export async function load({ cookies, fetch, parent, request }) {
    const wrappedFetch = wrapFetch({
        fetch,
        baseUrl: JUPYTERHUB_BASE_URL,
        cookieHeader: getCookieHeader(request),
        cookiePath: JUPYTERHUB_WEB_PREFIX,
        cookies,
        credentials: "include",
        ensureOk: true,
    })

    const response = await wrappedFetch(`${JUPYTERHUB_WEB_PREFIX}/hub/login`, { redirect: "manual" })

    // If the user is already logged in, return
    if (response.status == 302) {
        return
    }

    const $ = loadHtmlString(await response.text())
    const csrf = $("#login-main input[name=_xsrf]").attr("value")!

    const { userInfo } = await parent()
    const username = userInfo?.username ?? "anonymous"

    await wrappedFetch(`${JUPYTERHUB_WEB_PREFIX}/hub/login`, {
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
