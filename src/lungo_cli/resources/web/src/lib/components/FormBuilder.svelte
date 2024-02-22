<script lang="ts">
    import type { ActionResult } from "@sveltejs/kit"
    import { applyAction, enhance } from "$app/forms"
    import { page } from "$app/stores"
    import { PasswordInput } from "$lib/components"
    import type { KratosComponents } from "$lib/types"

    export let primaryGroup: KratosComponents["schemas"]["uiNode"]["group"] | undefined = undefined
    export let validationFreeButtons = [] as string[]

    const clipMessage = (msg: string) => {
        return msg.slice(0, msg.indexOf(".") + 1 || msg.length)
    }
    const getGroupActionTitle = (group: KratosComponents["schemas"]["uiNode"]["group"]) => {
        return (
            nodes
                .find((node) => node.group === group && node.type === "input" && node.attributes.type === "submit")
                ?.meta.label?.text.split(" with")[0] ?? ""
        )
    }
    const getNodeId = (node: KratosComponents["schemas"]["uiNode"]) => {
        if (node.type === "input") {
            return node.meta.label?.id ?? node.attributes.name + node.attributes.value
        } else {
            return node.attributes.id
        }
    }
    const noReload = () => {
        disabled = true

        return async ({ result }: { result: ActionResult }) => {
            // When the client is rate limited, the request won't make it to the node server
            if (result.type === "error") {
                result.status = 429
            }

            await applyAction(result)
            disabled = false
        }
    }

    let disabled = false
    let flow: string
    let actionNodes: KratosComponents["schemas"]["uiNodeInput"][]
    let messages: KratosComponents["schemas"]["uiTexts"]
    let nodes: KratosComponents["schemas"]["uiNodes"] = $page.data.nodes
    let currentGroup: KratosComponents["schemas"]["uiNode"]["group"] =
        primaryGroup && nodes.some((node) => node.group === primaryGroup)
            ? primaryGroup
            : nodes.find((node) => node.group !== "default")?.group ?? "default"
    let otherGroups: KratosComponents["schemas"]["uiNode"]["group"][]

    $: actionNodes = nodes.filter(
        (node) =>
            (node.group === "default" || node.group === currentGroup) &&
            node.type === "input" &&
            node.attributes.type === "submit"
    ) as KratosComponents["schemas"]["uiNodeInput"][]
    $: flow = $page.form?.flow ?? $page.data.flow
    $: messages = $page.form?.messages ?? $page.data.messages
    $: nodes = $page.form?.nodes ?? $page.data.nodes
    $: otherGroups = [
        ...new Set(nodes.map((node) => node.group).filter((group) => group !== "default" && group !== currentGroup)),
    ]
</script>

<form class="flex w-full flex-col gap-2" method="post" use:enhance={noReload}>
    <input class="input" name="flow" type="hidden" value={flow} />
    {#each nodes as node (getNodeId(node))}
        {#if node.group === "default" || node.group === currentGroup}
            {#if node.type === "input"}
                {#if node.attributes.type === "button"}
                    <!--  Not implemented  -->
                {:else if node.attributes.type === "checkbox"}
                    <!--  Not implemented  -->
                {:else if node.attributes.type === "password"}
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="inline-flex flex-col">
                        <PasswordInput
                            name={node.attributes.name}
                            value={node.attributes.value ?? ""}
                            disabled={node.attributes.disabled}
                            required={node.attributes.required}
                            autocomplete={node.attributes.autocomplete ?? "off"}
                            placeholder={node.meta.label?.text ?? ""}
                        />
                        {#each node.messages ?? [] as message (message.id)}
                            <span
                                class="mt-1 text-sm"
                                class:text-error={message.type === "error"}
                                class:text-success={message.type === "info" || message.type === "success"}
                            >
                                {clipMessage(message.text)}
                            </span>
                        {/each}
                    </label>
                {:else if node.attributes.type === "submit"}
                    <!--  Skip  -->
                {:else if node.meta.label}
                    <label class="inline-flex flex-col">
                        <input
                            class="input"
                            name={node.attributes.name}
                            type={node.attributes.type}
                            value={node.attributes.value ?? ""}
                            disabled={node.attributes.disabled}
                            required={node.attributes.required}
                            autocomplete={node.attributes.autocomplete ?? "off"}
                            placeholder={node.meta.label.text ?? ""}
                        />
                        {#each node.messages ?? [] as message (message.id)}
                            <span
                                class="mt-1 text-sm"
                                class:text-error={message.type === "error"}
                                class:text-success={message.type === "info" || message.type === "success"}
                            >
                                {clipMessage(message.text)}
                            </span>
                        {/each}
                    </label>
                {:else}
                    <input
                        class="input"
                        name={node.attributes.name}
                        type={node.attributes.type}
                        value={node.attributes.value ?? ""}
                        disabled={node.attributes.disabled}
                        required={node.attributes.required}
                        autocomplete={node.attributes.autocomplete ?? "off"}
                    />
                {/if}
            {/if}
        {/if}
    {/each}
    <slot />
    {#each messages ?? [] as message (message.id)}
        <span
            class="text-sm"
            class:text-error={message.type === "error"}
            class:text-success={message.type === "info" || message.type === "success"}
        >
            {clipMessage(message.text)}
        </span>
    {/each}
    <div class="my-3"></div>
    {#each actionNodes as actionNode (getNodeId(actionNode))}
        <button
            class="btn btn-primary"
            name={actionNode.attributes.name}
            type="submit"
            value={actionNode.attributes.value ?? ""}
            {disabled}
            formnovalidate={validationFreeButtons.includes(actionNode.attributes.name)}
        >
            {actionNode.meta.label?.text ?? ""}
        </button>
    {/each}
    {#each otherGroups as group (group)}
        <button
            class="btn btn-secondary"
            type="button"
            {disabled}
            on:click={() => {
                currentGroup = group
            }}
        >
            {getGroupActionTitle(group)} with {group}
        </button>
    {/each}
</form>
