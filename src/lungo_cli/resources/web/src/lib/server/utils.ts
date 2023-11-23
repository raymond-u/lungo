import { EApp } from "$lib/server/types"
import { type App, EIcon } from "$lib/types"

export function createApp(app: EApp): App {
    switch (app) {
        case EApp.FileBrowser:
            return { name: "File Browser", href: `/app/${EApp.FileBrowser}`, icon: EIcon.Folder }
        case EApp.PrivateBin:
            return { name: "Pastebin", href: `/app/${EApp.PrivateBin}`, icon: EIcon.Note }
        case EApp.JupyterHub:
            return { name: "JupyterHub", href: `/app/${EApp.JupyterHub}`, icon: EIcon.Jupyter }
        case EApp.RStudio:
            return { name: "RStudio", href: `/app/${EApp.RStudio}`, icon: EIcon.RStudio }
        case EApp.XRay:
            return { name: "Proxy", href: `/app/${EApp.XRay}`, icon: EIcon.Proxy }
    }
}
