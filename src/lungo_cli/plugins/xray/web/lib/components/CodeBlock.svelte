<script lang="ts">
    import "highlight.js/styles/atom-one-dark.min.css"
    import hljs from "highlight.js/lib/core"
    import json from "highlight.js/lib/languages/json"
    import yaml from "highlight.js/lib/languages/yaml"

    export let code: string
    export let language: string
    export let highlightedLines = [] as number[]
    export let lineNumbers = true

    const dedent = (text: string) => {
        const lines = text.match(/^(?:[ \t]*\n)*(.*?)\s*$/s)![1].split("\n")
        const minLeadingSpaces = lines.reduce((acc, line) => {
            if (line.match(/^\s*$/)) {
                return acc
            }

            const leadingSpaces = line.match(/^\s*/)![0].length
            return leadingSpaces < acc ? leadingSpaces : acc
        }, Infinity)

        return lines.map((line) => line.substring(minLeadingSpaces)).join("\n")
    }

    // Remember to register all the languages used in the code
    hljs.registerLanguage("json", json)
    hljs.registerLanguage("yaml", yaml)

    const lines = hljs
        .highlight(dedent(code), { language })
        .value.split("\n")
        .map((line, i) => ({ index: i, line, prefix: i + 1 }))
</script>

<div class="scrollbar-transparent mockup-code">
    {#each lines as { index, line, prefix }}
        {@const highlighted = highlightedLines.includes(index)}
        {@const symbol = lineNumbers ? prefix : undefined}
        <!--  eslint-disable-next-line svelte/no-at-html-tags  -->
        <pre class={highlighted ? "bg-warning/20" : ""} data-prefix={symbol}><code>{@html line}</code></pre>
    {/each}
</div>
