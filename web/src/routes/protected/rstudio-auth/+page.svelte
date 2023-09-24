<script context="module" lang="ts">
    declare function encrypt(payload: string, exp: string, mod: string): string
</script>

<script lang="ts">
    import { onMount } from "svelte"
    import { asSearchParams } from "$lib/utils"

    onMount(() => {
        const script = document.createElement("script")
        script.src = "/rstudio/js/encrypt.min.js"
        script.onload = async () => {
            const redirect = () => (window.location.href = "/rstudio/")

            try {
                let response = await fetch("/auth/api/state")

                if (!response.ok) {
                    return redirect()
                }

                const json = await response.json()
                const username = json["data"]["username"]
                const password = "passwd"
                const payload = `${username}\n${password}`

                response = await fetch("/rstudio/", { redirect: "manual" })

                // If the user is already logged in, redirect to the RStudio page
                if (response.ok) {
                    return redirect()
                }

                response = await fetch("/rstudio/auth-sign-in", { headers: { "X-Bypass": "1" } })

                if (!response.ok) {
                    return redirect()
                }

                let text = await response.text()

                const html = new DOMParser().parseFromString(text, "text/html")
                const key = html.getElementsByName("public-key-url")[0].getAttribute("content")

                response = await fetch(`/rstudio/${key}`)

                if (!response.ok) {
                    return redirect()
                }

                text = await response.text()
                const [exp, mod] = text.split(":", 2)

                ;(html.getElementById("clientPath") as HTMLInputElement).value = "/rstudio/auth-sign-in"
                ;(html.getElementById("package") as HTMLInputElement).value = encrypt(payload, exp, mod)
                ;(html.getElementById("persist") as HTMLInputElement).value = "0"

                response = await fetch("/rstudio/auth-do-sign-in", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-Bypass": "1",
                    },
                    redirect: "manual",
                    body: asSearchParams(html.getElementsByName("realform")[0] as HTMLFormElement),
                })
            } finally {
                redirect()
            }
        }

        document.head.appendChild(script)
    })
</script>
