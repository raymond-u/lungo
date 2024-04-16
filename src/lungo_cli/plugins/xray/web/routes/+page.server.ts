import { v5 as uuidv5 } from "uuid"
import {
    XRAY_DOMAIN_KEYWORD_WHITELIST,
    XRAY_DOMAIN_SUFFIX_WHITELIST,
    XRAY_DOMAIN_WHITELIST,
    XRAY_IP_RANGE_WHITELIST,
    XRAY_SALT,
    XRAY_WEB_PREFIX,
} from "$lib/plugins/xray/server/constants.server"

export async function load({ parent }) {
    const { userInfo } = await parent()
    const username = userInfo?.username ?? "anonymous"

    return {
        xrayDomainKeywordWhitelist: JSON.parse(XRAY_DOMAIN_KEYWORD_WHITELIST) as string[],
        xrayDomainSuffixWhitelist: JSON.parse(XRAY_DOMAIN_SUFFIX_WHITELIST) as string[],
        xrayDomainWhitelist: JSON.parse(XRAY_DOMAIN_WHITELIST) as string[],
        xrayId: uuidv5(username, XRAY_SALT),
        xrayIpRangeWhitelist: JSON.parse(XRAY_IP_RANGE_WHITELIST) as string[],
        xrayWebPrefix: XRAY_WEB_PREFIX,
    }
}
