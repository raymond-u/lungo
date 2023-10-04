import { fail, redirect } from "@sveltejs/kit"
import { invalidate } from "$app/navigation"
import { createKratosClient, type kratosComponents } from "$lib/api"
import { EDependency, type Fetch } from "$lib/types"
import { getFlow, getRandomId } from "$lib/utils"

export const actions = {
    default: async ({ request }: { request: Request }) => {
        const data = await request.formData()

        const client = createKratosClient(fetch)
        const response = await client.POST("/self-service/settings", {
            params: { query: { flow: data.get("flow") as string } },
            body: {
                csrf_token: data.get("csrf_token") as string,
                method: data.get("method") as string,
                password: data.get("password") as string,
            },
        })

        switch (response.response.status) {
            case 200:
                return {
                    messages: [
                        {
                            id: getRandomId(),
                            text: "Account information updated.",
                            type: "success",
                        },
                    ],
                }
            case 303:
                await invalidate(EDependency.Form)
                return fail(400, {
                    messages: [
                        {
                            id: getRandomId(),
                            text: "Session expired. Please try again.",
                            type: "error",
                        },
                    ],
                })
            case 400:
                return fail(400, {
                    messages: (response.error as kratosComponents["schemas"]["settingsFlow"]).ui.messages,
                    nodes: (response.error as kratosComponents["schemas"]["settingsFlow"]).ui.nodes,
                })
            default:
                await invalidate(EDependency.Form)
                return fail(400, {
                    messages: [
                        {
                            id: getRandomId(),
                            text: (response.error as kratosComponents["schemas"]["errorGeneric"]).error.message,
                            type: "error",
                        },
                    ],
                })
        }
    },
}

export async function load({ depends, fetch }: { depends: (...deps: string[]) => void; fetch: Fetch }) {
    depends(EDependency.Form)

    // const client = createKratosClient(fetch)
    // const response = await client.GET("/self-service/settings/browser", { params: {} })
    //
    // switch (response.response.status) {
    //     case 200:
    //         return {
    //             flow: getFlow(response.data!.ui.action),
    //             messages: response.data!.ui.messages,
    //             nodes: response.data!.ui.nodes,
    //         }
    //     default:
    //         // Invalid session or insufficient session privileges
    //         throw redirect(302, "/login")
    // }

    return {
        flow: getFlow("https://playground.com/self-service/login?flow=33f6079a-ef14-4084-af13-34a91e53cd6c"),
        messages: [],
        nodes: [
            {
                type: "input",
                group: "default",
                attributes: {
                    name: "csrf_token",
                    type: "hidden",
                    value: "XmG3qwTYSV0oWIyNGTugvtNOKMxWPYHd7dNX7BYK5lL79P0iUdq5jVmRUKwwm8RLcAGN7eF7iYraAiTSOdamuQ==",
                    required: true,
                    disabled: false,
                },
                messages: [],
                meta: {},
            },
            {
                type: "input",
                group: "password",
                attributes: {
                    name: "password",
                    type: "password",
                    required: true,
                    disabled: false,
                },
                messages: [],
                meta: {
                    label: {
                        id: 1070001,
                        text: "Password",
                        type: "info",
                    },
                },
            },
            {
                type: "input",
                group: "password",
                attributes: {
                    name: "method",
                    type: "submit",
                    value: "password",
                    disabled: false,
                },
                messages: [],
                meta: {
                    label: {
                        id: 1010001,
                        text: "Change password",
                        type: "info",
                        context: {},
                    },
                },
            },
        ],
    }
}
