export function capitalize(text: string): string {
    return `${text[0]?.toUpperCase() ?? ""}${text.slice(1)}`
}

export function concatenateUrl(path: string | URL, baseUrl: string | URL): string {
    let baseUrlString: string
    let pathString: string

    if (typeof baseUrl === "string") {
        baseUrlString = baseUrl
    } else {
        baseUrlString = baseUrl.origin + baseUrl.pathname
    }

    if (baseUrlString.endsWith("/")) {
        baseUrlString = baseUrlString.slice(0, -1)
    }

    if (typeof path === "string" && !path.match("https?://")) {
        if (path.startsWith("/")) {
            pathString = path
        } else {
            pathString = "/" + path
        }
    } else {
        const pathUrl = new URL(path)
        pathString = pathUrl.pathname + pathUrl.search + pathUrl.hash
    }

    return baseUrlString + pathString
}

export function getFlowId(url: string): string {
    return new URL(url).searchParams.get("flow") ?? ""
}

export function getNameInitials(firstName: string, lastName: string): string {
    return `${firstName[0]?.toUpperCase() ?? ""}${lastName[0]?.toUpperCase() ?? ""}`
}

export function getRandomElement<T>(array: T[]): T {
    return array[Math.floor(Math.random() * array.length)]
}

export function getRandomId(): number {
    return Number(Math.round(Math.random() * 100000).toString() + Date.now().toString().slice(-5))
}

export function getUrlParts(url: string): { path: string; query: string; hash: string } {
    const [path, other] = url.split("?", 2)

    if (other) {
        const [query, hash] = other.split("#", 2)

        return {
            path,
            query: `?${query}`,
            hash: hash ? `#${hash}` : "",
        }
    }

    return {
        path,
        query: "",
        hash: "",
    }
}

export function isSameHost(url: string | URL, host: string): boolean {
    if (typeof url === "string" && !url.match("^(?:https?|wss?)://")) {
        return true
    }

    return new URL(url).host === host
}

export function truncate(text: string, length: number): string {
    if (text.length > length) {
        const capitalSplit = text[0] + text.slice(1).split(/[A-Z]/)[0]
        const spaceSplit = text.split(" ")[0]

        return capitalSplit.length < spaceSplit.length ? capitalSplit : spaceSplit
    } else {
        return text
    }
}
