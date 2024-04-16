from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginConfig


class Plugin(BasePlugin[BaseSettings]):
    config = PluginConfig(
        name="filebrowser",
        descriptive_name="File Browser",
        version="0.1.0",
        description="File Browser as a Lungo plugin.",
        compatible_with="~=0.3.0",
        have_backend=True,
        backend_port=80,
        require_account=True,
        web_icon="icons/FolderOutline.svelte",
        web_alt_icon="icons/FolderSolid.svelte",
    )

    @override
    def get_render_context(self) -> dict[str, Any]:
        return {
            "filebrowser_default_password_hash": "$2a$10$aulj1r/ROe0VnA1iE2/ojOItBBFeHK0KLMv5mnl3ECXfiNLKfcKHi",
            "filebrowser_version": "v2.27.0",
        }