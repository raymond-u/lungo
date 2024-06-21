from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="filebrowser",
        version="0.3.0",
        descriptive_name="File Browser",
        description="File Browser as a Lungo plugin.",
        compatible_with="~=0.5.0",
        have_backend=True,
        backend_port=80,
        require_account=True,
        web_icon="icons/FolderOutline.svelte",
        web_alt_icon="icons/FolderSolid.svelte",
    )

    @override
    def get_custom_rendering_context(self) -> dict[str, Any]:
        return {
            "filebrowser_default_password_hash": "$2a$10$aulj1r/ROe0VnA1iE2/ojOItBBFeHK0KLMv5mnl3ECXfiNLKfcKHi",
            "filebrowser_version": "v2.30.0",
        }
