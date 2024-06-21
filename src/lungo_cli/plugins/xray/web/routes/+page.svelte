<script lang="ts">
    import { BASE_URL } from "$lib/constants"
    import { CodeBlock } from "$lib/plugins/xray/components"
    import { NetworkLockIcon } from "$lib/plugins/xray/icons"

    export let data

    const hostname = new URL(BASE_URL).hostname
    const port = new URL(BASE_URL).port || "443"

    const clashConfig = `
        proxies:
          - name: VPN
            type: vless
            server: ${hostname}
            port: ${port}
            uuid: "${data.xrayId}"
            tls: true
            skip-cert-verify: true
            udp: true
            network: ws
            ws-opts:
              path: ${data.xrayWebPrefix}
    `
    const xrayConfig = `
        "outbounds": [
          {
            "tag": "VPN",
            "protocol": "vless",
            "settings": {
              "vnext": [
                {
                  "address": "${hostname}",
                  "port": ${port},
                  "users": [
                    {
                      "id": "${data.xrayId}",
                      "encryption": "none"
                    }
                  ]
                }
              ]
            },
            "streamSettings": {
              "network": "ws",
              "security": "tls",
              "tlsSettings": {
                "allowInsecure": true,
              },
              "wsSettings": {
                "path": "${data.xrayWebPrefix}"
              }
            }
          }
        ]
    `

    let clashRules = [] as string[]
    let xrayRules = { routing: { rules: [] } } as {
        routing: {
            rules: (
                | { type: string; domain: string[]; outboundTag: string }
                | { type: string; ip: string[]; outboundTag: string }
            )[]
        }
    }

    if (
        data.xrayDomainWhitelist.length ||
        data.xrayDomainKeywordWhitelist.length ||
        data.xrayDomainSuffixWhitelist.length ||
        data.xrayIpRangeWhitelist.length
    ) {
        clashRules.push("rules:")

        for (const domain of data.xrayDomainWhitelist) {
            clashRules.push(`  - DOMAIN,${domain},VPN`)
        }
        for (const domainKeyword of data.xrayDomainKeywordWhitelist) {
            clashRules.push(`  - DOMAIN-KEYWORD,${domainKeyword},VPN`)
        }
        for (const domainSuffix of data.xrayDomainSuffixWhitelist) {
            clashRules.push(`  - DOMAIN-SUFFIX,${domainSuffix},VPN`)
        }
        for (const ipRange of data.xrayIpRangeWhitelist) {
            clashRules.push(`  - IP-CIDR,${ipRange},VPN,no-resolve`)
        }
    }

    if (data.xrayDomainWhitelist.length || data.xrayDomainKeywordWhitelist.length || data.xrayDomainSuffixWhitelist.length) {
        xrayRules.routing.rules.push({
            type: "field",
            domain: [
                ...data.xrayDomainWhitelist.map((x) => `full:${x}`),
                ...data.xrayDomainKeywordWhitelist,
                ...data.xrayDomainSuffixWhitelist.map((x) => `domain:${x}`),
            ],
            outboundTag: "VPN",
        })
    }

    if (data.xrayIpRangeWhitelist.length) {
        xrayRules.routing.rules.push({
            type: "field",
            ip: data.xrayIpRangeWhitelist,
            outboundTag: "VPN",
        })
    }
</script>

<div class="flex flex-1 flex-col items-center">
    <div class="prose flex max-w-md flex-col items-center px-4 py-8 md:max-w-2xl md:px-8 md:py-16">
        <div class="flex flex-col items-center">
            <span class="h-24 w-24 py-2">
                <NetworkLockIcon />
            </span>
            <h1 class="text-center">Connecting to the VPN Server</h1>
        </div>
        <p>
            This note helps you connect to the private network where the host is located. Please select your preferred
            proxy client:
        </p>
        <div class="tabs tabs-lifted">
            <input
                class="tab [--tab-border-color:var(--fallback-nc,oklch(var(--nc)))]"
                type="radio"
                name="proxy-client"
                aria-label="Clash"
                checked
            />
            <div class="tab-content max-w-md rounded-box border-neutral-content px-4 md:max-w-xl md:px-8 lg:max-w-4xl">
                <ol>
                    <li>
                        <p>
                            Add server information to the configuration file. Omit the highlighted part if not using a
                            self-signed TLS certificate on the website.
                        </p>
                        <div class="not-prose my-5">
                            <CodeBlock code={clashConfig} highlightedLines={[7]} language="yaml" />
                        </div>
                    </li>
                    {#if clashRules.length}
                        <li>
                            <p>
                                Configure rules to forward requests to the internal network. Here is a minimal example.
                            </p>
                            <div class="not-prose my-5">
                                <CodeBlock code={clashRules.join("\n")} language="yaml" />
                            </div>
                        </li>
                    {/if}
                </ol>
            </div>
            <input
                class="tab [--tab-border-color:var(--fallback-nc,oklch(var(--nc)))]"
                type="radio"
                name="proxy-client"
                aria-label="Xray"
            />
            <div class="tab-content max-w-md rounded-box border-neutral-content px-4 md:max-w-xl md:px-8 lg:max-w-4xl">
                <ol>
                    <li>
                        <p>
                            Add server information to the configuration file. Omit the highlighted part if not using a
                            self-signed TLS certificate on the website.
                        </p>
                        <div class="not-prose my-5">
                            <CodeBlock code={xrayConfig} highlightedLines={[21, 22, 23]} language="json" />
                        </div>
                    </li>
                    {#if xrayRules.routing.rules.length}
                        <li>
                            <p>
                                Configure rules to forward requests to the internal network. Here is a minimal example.
                            </p>
                            <div class="not-prose my-5">
                                <CodeBlock code={JSON.stringify(xrayRules, null, 2)} language="json" />
                            </div>
                        </li>
                    {/if}
                </ol>
            </div>
        </div>
    </div>
</div>
