import { v5 as uuidv5 } from "uuid"
import { XRAY_SALT } from "$lib/server/constants"
import type { User } from "$lib/types"

export async function load({ parent }: { parent: () => Promise<{ userInfo: User["traits"] | undefined }> }) {
    const { userInfo } = await parent()
    const username = userInfo?.username ?? "anonymous"

    return {
        xrayId: uuidv5(username, XRAY_SALT!),
    }
}
