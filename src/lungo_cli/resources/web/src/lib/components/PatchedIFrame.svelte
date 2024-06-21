<script lang="ts">
    import parser from "set-cookie-parser"
    import { onMount } from "svelte"
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { getUrlParts, isSameHost, useStore } from "$lib/utils"

    const { currentApp, currentIFrame } = useStore()

    const getOriginalUrl = (url: string | URL) => {
        if (typeof url === "string") {
            const { path, query, hash } = getUrlParts(url)
            const params = new URLSearchParams(query)
            params.delete("iframe", "1")

            if (params.size > 0) {
                return `${path}?${params.toString()}${hash}`
            }

            return `${path}${hash}`
        } else {
            const newUrl = new URL(url.href)
            newUrl.searchParams.delete("iframe", "1")

            return newUrl.href
        }
    }

    const getModifiedUrl = (url: string | URL) => {
        if (typeof url === "string") {
            const { path, query, hash } = getUrlParts(url)
            const params = new URLSearchParams(query)
            params.set("iframe", "1")

            return `${path}?${params.toString()}${hash}`
        } else {
            const newUrl = new URL(url.href)
            newUrl.searchParams.set("iframe", "1")

            return newUrl.href
        }
    }

    const handleLoad = (e: Event) => {
        const iframe = e.target as HTMLIFrameElement
        const open = iframe.contentWindow!.open.bind(iframe.contentWindow!)
        const pushState = iframe.contentWindow!.history.pushState.bind(iframe.contentWindow!.history)
        const replaceState = iframe.contentWindow!.history.replaceState.bind(iframe.contentWindow!.history)
        // @ts-expect-error type definition is inaccurate
        const cookie = Object.getOwnPropertyDescriptor(iframe.contentWindow!.Document.prototype, "cookie")!
        const getCookie = cookie.get!.bind(iframe.contentDocument)
        const setCookie = cookie.set!.bind(iframe.contentDocument)

        // In case the History API is called before the iframe is loaded
        if (!iframe.contentWindow!.location.search.includes("iframe=1")) {
            replaceState(null, "", getModifiedUrl(iframe.contentWindow!.location.href))
        }

        goto(getOriginalUrl(iframe.contentWindow!.location.href), { replaceState: true })

        // Patch the History API
        iframe.contentWindow!.history.pushState = (
            data: Parameters<typeof pushState>[0],
            unused: Parameters<typeof pushState>[1],
            url: Parameters<typeof pushState>[2] = undefined
        ) => {
            if (url) {
                goto(getOriginalUrl(url), { replaceState: true })
                pushState(data, unused, getModifiedUrl(url))
            } else {
                pushState(data, unused)
            }
        }
        iframe.contentWindow!.history.replaceState = (
            data: Parameters<typeof replaceState>[0],
            unused: Parameters<typeof replaceState>[1],
            url: Parameters<typeof replaceState>[2] = undefined
        ) => {
            if (url) {
                goto(getOriginalUrl(url), { replaceState: true })
                replaceState(data, unused, getModifiedUrl(url))
            } else {
                replaceState(data, unused)
            }
        }

        // Patch the open() method
        iframe.contentWindow!.open = (
            url: Parameters<typeof open>[0] = undefined,
            target: Parameters<typeof open>[1] = undefined,
            windowFeatures: Parameters<typeof open>[2] = undefined
        ) => {
            if (url) {
                if (isSameHost(url, $page.url.host)) {
                    url = getModifiedUrl(url)
                    target = "_self"
                }

                if (target === "_top") {
                    target = "_self"
                }

                return open(url, target, windowFeatures)
            } else {
                return open(url, target, windowFeatures)
            }
        }

        // Patch all links
        for (const node of iframe.contentDocument!.querySelectorAll("a, area, base, form")) {
            if (
                node instanceof HTMLAnchorElement ||
                node instanceof HTMLAreaElement ||
                node instanceof HTMLBaseElement
            ) {
                if (isSameHost(node.href, $page.url.host)) {
                    node.href = getModifiedUrl(node.href)
                    node.target = "_self"
                }

                if (node.target === "_top") {
                    node.target = "_self"
                }
            } else if (node instanceof HTMLFormElement) {
                if (node.target === "_blank" || node.target === "_top") {
                    node.target = "_self"
                }
            }
        }

        // Patch the cookie setter
        Object.defineProperty(iframe.contentDocument, "cookie", {
            get: getCookie,
            set: (value: string) => {
                const old = parser.parse(value, { decodeValues: false })[0]
                let newCookie = `${old.name}=${old.value}; Path=${$currentApp?.href ?? "/"}; SameSite=Lax; Secure`

                if (old.expires) {
                    newCookie += `; Expires=${old.expires.toUTCString()}`
                }
                if (old.maxAge) {
                    newCookie += `; Max-Age=${old.maxAge}`
                }
                if (old.httpOnly) {
                    newCookie += "; HttpOnly"
                }

                setCookie(newCookie)
            },
        })
    }

    let iFrame: HTMLIFrameElement | undefined

    onMount(() => {
        $currentIFrame = iFrame
        iFrame!.addEventListener("load", handleLoad)
        iFrame!.src = getModifiedUrl($page.url)

        const unsubscribe = currentApp.subscribe((value) => {
            if (value) {
                if (!iFrame!.src.match(`^(?:https?://[^/]+)?${value.href}`)) {
                    iFrame!.src = value.href + "?iframe=1"
                }
            }
        })

        return () => {
            unsubscribe()
            iFrame!.removeEventListener("load", handleLoad)
            $currentIFrame = undefined
        }
    })
</script>

{#if $page.data.apps.length > 0}
    <div class="size-full border-t-2 border-base-content/20 md:border-l-2">
        <iframe title={$currentApp?.name ?? ""} class="size-full" bind:this={iFrame} />
    </div>
{:else}
    <div class="size-full border-t-2 border-base-content/20">
        <iframe title={$currentApp?.name ?? ""} class="size-full" bind:this={iFrame} />
    </div>
{/if}
