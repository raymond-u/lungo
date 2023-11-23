<script lang="ts">
    import { CodeBlock } from "$lib/components"
    import {
        HOSTNAME,
        HTTPS_PORT,
        XRAY_DOMAIN_KEYWORD_WHITELIST,
        XRAY_DOMAIN_SUFFIX_WHITELIST,
        XRAY_DOMAIN_WHITELIST,
        XRAY_IP_RANGE_WHITELIST,
    } from "$lib/constants"
    import { NetworkLockIcon } from "$lib/icons"

    export let data

    const clash_config = `
        proxies:
          - name: VPN
            type: vless
            server: ${HOSTNAME}
            port: ${HTTPS_PORT}
            uuid: "${data.xrayId}"
            tls: true
            skip-cert-verify: true
            udp: true
            network: ws
            ws-opts:
              path: /app/xray
    `
    const xray_config = `
        "outbounds": [
          {
            "tag": "VPN",
            "protocol": "vless",
            "settings": {
              "vnext": [
                {
                  "address": "${HOSTNAME}",
                  "port": ${HTTPS_PORT},
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
                "path": "/app/xray"
              }
            }
          }
        ]
    `

    let clash_rules = [] as string[]
    let xray_rules = { routing: { rules: [] } } as {
        routing: {
            rules: (
                | { type: string; domain: string[]; outboundTag: string }
                | { type: string; ip: string[]; outboundTag: string }
            )[]
        }
    }

    const domain_whitelist = JSON.parse(XRAY_DOMAIN_WHITELIST!) as string[]
    const domain_keyword_whitelist = JSON.parse(XRAY_DOMAIN_KEYWORD_WHITELIST!) as string[]
    const domain_suffix_whitelist = JSON.parse(XRAY_DOMAIN_SUFFIX_WHITELIST!) as string[]
    const ip_range_whitelist = JSON.parse(XRAY_IP_RANGE_WHITELIST!) as string[]

    if (
        domain_whitelist.length ||
        domain_keyword_whitelist.length ||
        domain_suffix_whitelist.length ||
        ip_range_whitelist.length
    ) {
        clash_rules.push("rules:")

        for (const domain of domain_whitelist) {
            clash_rules.push(`  - DOMAIN,${domain},VPN`)
        }
        for (const domain_keyword of domain_keyword_whitelist) {
            clash_rules.push(`  - DOMAIN-KEYWORD,${domain_keyword},VPN`)
        }
        for (const domain_suffix of domain_suffix_whitelist) {
            clash_rules.push(`  - DOMAIN-SUFFIX,${domain_suffix},VPN`)
        }
        for (const ip_range of ip_range_whitelist) {
            clash_rules.push(`  - IP-CIDR,${ip_range},VPN,no-resolve`)
        }
    }

    if (domain_whitelist.length || domain_keyword_whitelist.length || domain_suffix_whitelist.length) {
        xray_rules.routing.rules.push({
            type: "field",
            domain: [
                ...domain_whitelist.map((x) => `full:${x}`),
                ...domain_keyword_whitelist,
                ...domain_suffix_whitelist.map((x) => `domain:${x}`),
            ],
            outboundTag: "VPN",
        })
    }

    if (ip_range_whitelist.length) {
        xray_rules.routing.rules.push({
            type: "field",
            ip: ip_range_whitelist,
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
                class="tab [--tab-border-color:oklch(var(--nc))]"
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
                            <CodeBlock code={clash_config} highlightedLines={[7]} language="yaml" />
                        </div>
                    </li>
                    {#if clash_rules.length}
                        <li>
                            <p>
                                Configure rules to forward requests to the internal network. Here is a minimal example.
                            </p>
                            <div class="not-prose my-5">
                                <CodeBlock code={clash_rules.join("\n")} language="yaml" />
                            </div>
                        </li>
                    {/if}
                </ol>
            </div>
            <input
                class="tab [--tab-border-color:oklch(var(--nc))]"
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
                            <CodeBlock code={xray_config} highlightedLines={[21, 22, 23]} language="json" />
                        </div>
                    </li>
                    {#if xray_rules.routing.rules.length}
                        <li>
                            <p>
                                Configure rules to forward requests to the internal network. Here is a minimal example.
                            </p>
                            <div class="not-prose my-5">
                                <CodeBlock code={JSON.stringify(xray_rules, null, 2)} language="json" />
                            </div>
                        </li>
                    {/if}
                </ol>
            </div>
        </div>
    </div>
</div>
