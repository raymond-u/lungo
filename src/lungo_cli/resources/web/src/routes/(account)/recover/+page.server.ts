import { type Cookies, fail, redirect } from "@sveltejs/kit"
import { createKratosClient } from "$lib/server/api"
import type { KratosComponents } from "$lib/types"
import { getFlow, getRandomId } from "$lib/utils"

export const actions = {
    default: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
        const data = await request.formData()

        const client = createKratosClient(cookies, fetch)
        const response = await client.POST("/self-service/recovery", {
            params: { query: { flow: data.get("flow") as string } },
            body: {
                csrf_token: data.get("csrf_token") as string,
                method: data.get("method") as "code" | "link",
                ...(data.get("email") ? { email: data.get("email") as string } : { code: data.get("code") as string }),
            },
        })

        switch (response.response.status) {
            case 200:
                if (!data.get("email")) {
                    throw redirect(302, "/account")
                }

                return {
                    flow: getFlow(response.data!.ui.action),
                    messages: response.data!.ui.messages,
                    nodes: response.data!.ui.nodes,
                }
            case 303:
                return fail(400, {
                    messages: [
                        {
                            id: getRandomId(),
                            text: "Session expired. Please refresh the page and try again.",
                            type: "error",
                        },
                    ],
                })
            case 400:
                return fail(400, {
                    flow: getFlow((response.error as KratosComponents["schemas"]["recoveryFlow"]).ui.action),
                    messages: (response.error as KratosComponents["schemas"]["recoveryFlow"]).ui.messages,
                    nodes: (response.error as KratosComponents["schemas"]["recoveryFlow"]).ui.nodes,
                })
            case 422:
                if (!data.get("email")) {
                    throw redirect(302, "/account")
                }

                break
            default:
                return fail(400, {
                    messages: [
                        {
                            id: getRandomId(),
                            text: (response.error as KratosComponents["schemas"]["errorGeneric"]).error.message,
                            type: "error",
                        },
                    ],
                })
        }
    },
}

export async function load({ cookies, fetch }: { cookies: Cookies; fetch: typeof global.fetch }) {
    const client = createKratosClient(cookies, fetch)
    const response = await client.GET("/self-service/recovery/browser", { params: {} })

    switch (response.response.status) {
        case 200:
            return {
                flow: getFlow(response.data!.ui.action),
                messages: response.data!.ui.messages,
                nodes: response.data!.ui.nodes,
            }
        default:
            // Already logged in
            throw redirect(302, "/account")
    }

    // return {
    //     flow: getFlow("https://playground.com/self-service/login?flow=33f6079a-ef14-4084-af13-34a91e53cd6c"),
    //     messages: [
    //         // {
    //         //     id: 4000001,
    //         //     text: "Wrong credentials.",
    //         //     type: "error",
    //         // },
    //     ],
    //     nodes: [
    //         {
    //             type: "input",
    //             group: "default",
    //             attributes: {
    //                 name: "csrf_token",
    //                 type: "hidden",
    //                 value: "csrf",
    //                 required: true,
    //                 disabled: false,
    //             },
    //             messages: [],
    //             meta: {},
    //         },
    //         {
    //             type: "input",
    //             group: "default",
    //             attributes: {
    //                 name: "email",
    //                 type: "text",
    //                 required: true,
    //                 disabled: false,
    //             },
    //             messages: [],
    //             meta: {
    //                 label: {
    //                     id: 1070001,
    //                     text: "Email",
    //                     type: "info",
    //                 },
    //             },
    //         },
    //         {
    //             type: "input",
    //             group: "default",
    //             attributes: {
    //                 name: "method",
    //                 type: "submit",
    //                 value: "code",
    //                 disabled: false,
    //             },
    //             messages: [],
    //             meta: {
    //                 label: {
    //                     id: 1010001,
    //                     text: "Send recovery code",
    //                     type: "info",
    //                     context: {},
    //                 },
    //             },
    //         },
    //     ],
    // }
}
