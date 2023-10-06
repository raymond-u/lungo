<script lang="ts">
    import type { ActionResult } from "@sveltejs/kit"
    import { applyAction, enhance } from "$app/forms"
    import { page } from "$app/stores"
    import { PasswordInput } from "$lib/components"
    import type { KratosComponents } from "$lib/types"

    const getNodeId = (node: KratosComponents["schemas"]["uiNode"]) => {
        if (node.type === "input") {
            return node.meta.label?.id ?? node.attributes.name + node.attributes.value
        } else {
            return node.attributes.id
        }
    }
    const getSwitchGroupTitle = (group: KratosComponents["schemas"]["uiNode"]["group"]) => {
        return (
            nodes.find((node) => node.group === group && node.type === "input" && node.attributes.type === "submit")
                ?.meta.label?.text ?? ""
        )
    }
    const noReload = () => {
        disabled = true

        return async ({ result }: { result: ActionResult }) => {
            await applyAction(result)
            disabled = false
        }
    }

    let disabled = false
    let flow = $page.data.flow

    let messages: KratosComponents["schemas"]["uiTexts"] = $page.data.messages
    let nodes: KratosComponents["schemas"]["uiNodes"] = $page.data.nodes
    let currentGroup: KratosComponents["schemas"]["uiNode"]["group"] =
        nodes.find((node) => node.group !== "default")?.group ?? "default"
    let otherGroups: KratosComponents["schemas"]["uiNode"]["group"][]

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
                    <!--  TODO  -->
                {:else if node.attributes.type === "checkbox"}
                    <!--  TODO  -->
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
                                class:text-success={message.type === "success"}
                            >
                                {message.text}
                            </span>
                        {/each}
                    </label>
                {:else if node.attributes.type === "submit"}
                    <slot />
                    {#each messages ?? [] as message (message.id)}
                        <span
                            class="text-sm"
                            class:text-error={message.type === "error"}
                            class:text-success={message.type === "success"}
                        >
                            {message.text}
                        </span>
                    {/each}
                    <button
                        class="btn btn-primary mt-8"
                        name={node.attributes.name}
                        type={node.attributes.type}
                        value={node.attributes.value ?? ""}
                        {disabled}
                    >
                        {node.meta.label?.text ?? ""}
                    </button>
                {:else if node.meta.label}
                    <label class="inline-flex flex-col">
                        <input
                            name={node.attributes.name}
                            type={node.attributes.type}
                            value={node.attributes.value ?? ""}
                            disabled={node.attributes.disabled}
                            required={node.attributes.required}
                            autocomplete={node.attributes.autocomplete ?? "off"}
                            placeholder={node.meta.label.text ?? ""}
                            class="input"
                        />
                        {#each node.messages ?? [] as message (message.id)}
                            <span
                                class="mt-1 text-sm"
                                class:text-error={message.type === "error"}
                                class:text-success={message.type === "success"}
                            >
                                {message.text}
                            </span>
                        {/each}
                    </label>
                {:else}
                    <input
                        name={node.attributes.name}
                        type={node.attributes.type}
                        value={node.attributes.value ?? ""}
                        disabled={node.attributes.disabled}
                        required={node.attributes.required}
                        autocomplete={node.attributes.autocomplete ?? "off"}
                        class="input"
                    />
                {/if}
            {/if}
        {/if}
    {/each}
    {#each otherGroups as group (group)}
        <button
            class="btn btn-secondary"
            {disabled}
            on:click|preventDefault={() => {
                currentGroup = group
            }}
        >
            {getSwitchGroupTitle(group)} with {group}
        </button>
    {/each}
</form>
