import type { ComponentType } from "svelte"
import { QuestionMarkIcon } from "$lib/icons"
import { APP_INFO } from "$lib/server/constants"
import type { AppInfo, RawAppInfo } from "$lib/types"

let parsedApps: string[]
const parsedAppInfo: { [key: string]: AppInfo } = {}

export async function getAllApps(): Promise<string[]> {
    if (!parsedApps) {
        parsedApps = (JSON.parse(APP_INFO!) as RawAppInfo[]).map((app) => app.name).sort()
    }

    return parsedApps
}

export async function getAppInfo(name: string): Promise<AppInfo> {
    if (parsedAppInfo[name]) {
        return parsedAppInfo[name]
    }

    const rawAppInfo = (JSON.parse(APP_INFO!) as RawAppInfo[]).find((app) => app.name === name)!

    let icon: ComponentType
    let altIcon: ComponentType

    if (rawAppInfo.icon) {
        icon = (await import(`$lib/plugins/${name}/icons/${rawAppInfo.icon}`)).default
    } else {
        icon = QuestionMarkIcon
    }

    if (rawAppInfo.altIcon) {
        altIcon = (await import(`$lib/plugins/${name}/icons/${rawAppInfo.altIcon}`)).default
    } else {
        altIcon = icon
    }

    const appInfo = {
        name: rawAppInfo.name,
        descriptiveName: rawAppInfo.descriptiveName ?? rawAppInfo.name,
        href: `/app/${rawAppInfo.name}`,
        icon,
        altIcon,
    }
    parsedAppInfo[name] = appInfo

    return appInfo
}
