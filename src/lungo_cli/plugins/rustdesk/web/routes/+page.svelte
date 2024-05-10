<script lang="ts">
    import { ScreenCastIcon } from "$lib/plugins/rustdesk/icons"

    export let data
</script>

<div class="flex flex-1 flex-col items-center">
    <div class="prose flex max-w-md flex-col items-center px-4 py-8 md:max-w-2xl md:px-8 md:py-16">
        <div class="flex flex-col items-center">
            <span class="h-24 w-24 py-2">
                <ScreenCastIcon />
            </span>
            <h1 class="text-center">Using the RustDesk Relay Server</h1>
        </div>
        <p>
            This is a step-by-step guide on using the on-site RustDesk relay server for remote desktop access. Please
            note that you must be connected to the same network as the host machine to use the relay server.
        </p>
        <ol>
            <li>
                <p>Launch the RustDesk application.</p>
            </li>
            <li>
                <p>Click on the menu button to access the Settings page, and then navigate to the Network tab.</p>
            </li>
            <li>
                <p>
                    Enter
                    <code>{data.rustdeskLocalIp}</code>
                    in the ID Server input box.
                </p>
            </li>
            <li>
                <p>
                    Enter
                    <code>{data.rustdeskPublicKey}</code>
                    in the Key input box.
                </p>
            </li>
            <li>
                <p>Return to the Home page and enter a remote ID to access the desired remote desktop.</p>
            </li>
        </ol>
    </div>
</div>
