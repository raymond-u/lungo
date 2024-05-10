import { RUSTDESK_LOCAL_IP, RUSTDESK_PUBLIC_KEY } from "$lib/plugins/rustdesk/server/constants.server"

export async function load() {
    return {
        rustdeskLocalIp: RUSTDESK_LOCAL_IP,
        rustdeskPublicKey: RUSTDESK_PUBLIC_KEY,
    }
}
