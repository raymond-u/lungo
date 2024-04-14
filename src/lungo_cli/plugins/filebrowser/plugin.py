from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginConfig


class Plugin(BasePlugin[BaseSettings]):
    config = PluginConfig(
        name="filebrowser",
        descriptive_name="File Browser",
        version="0.1.0",
        description="File Browser as a Lungo plugin.",
        compatible_with="~=0.3.0",
        have_backend=True,
        require_account=True,
        web_icon="icons/FolderOutline.svelte",
        web_alt_icon="icons/FolderSolid.svelte",
    )
