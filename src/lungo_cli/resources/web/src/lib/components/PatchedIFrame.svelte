<script lang="ts">
    import parser from "set-cookie-parser"
    import { onMount } from "svelte"
    import { goto } from "$app/navigation"
    import { page } from "$app/stores"
    import { getUrlParts, isSameHost, useStore } from "$lib/utils"

    const { currentApp, currentIFrame } = useStore()

    const getOriginalUrl = (url: string | URL) => {
        if (typeof url === "string") {
            let { path, query, hash } = getUrlParts(url)
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

    const patchRedirects = (parentNode: HTMLElement) => {
        for (const childNode of parentNode.querySelectorAll("a, area, base, form")) {
            // Do not use `instanceof` here because the element might be from a different global context
            if (childNode.tagName === "A" || childNode.tagName === "AREA" || childNode.tagName === "BASE") {
                const node = childNode as HTMLAnchorElement | HTMLAreaElement | HTMLBaseElement

                if (node.target === "_top") {
                    node.target = "_self"
                } else if (isSameHost(node.href, $page.url.host) && node.target === "_blank") {
                    node.target = "_self"
                }
            } else if (childNode.tagName === "FORM") {
                const node = childNode as HTMLFormElement

                if (node.target === "_blank" || node.target === "_top") {
                    node.target = "_self"
                }
            }

            if (childNode.tagName === "A") {
                childNode.removeAttribute("referrerpolicy")
            }

            if (childNode.tagName === "A" || childNode.tagName === "AREA" || childNode.tagName === "FORM") {
                const node = childNode as HTMLAnchorElement | HTMLAreaElement | HTMLFormElement
                node.relList.remove("noreferrer")
            }
        }
    }

    let observer: MutationObserver

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
                if (target === "_top") {
                    target = "_self"
                } else if (isSameHost(url, $page.url.host) && target === "_blank" && !windowFeatures) {
                    url = getModifiedUrl(url)
                    target = "_self"
                }

                return open(url, target, windowFeatures)
            } else {
                return open(url, target, windowFeatures)
            }
        }

        // Patch all redirects
        patchRedirects(iframe.contentDocument!.body)
        observer.observe(iframe.contentDocument!.body, {
            childList: true,
            subtree: true,
        })

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
        observer = new MutationObserver((mutations: MutationRecord[]) => {
            const parentElements = new Set<HTMLElement>()

            for (const mutation of mutations) {
                const parentElement = mutation.addedNodes[0]?.parentElement

                if (parentElement) {
                    parentElements.add(parentElement)
                }
            }

            for (const parentElement of parentElements) {
                patchRedirects(parentElement)
            }
        })
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
            observer.disconnect()
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
