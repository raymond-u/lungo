from lungo_cli.core.plugin import BasePlugin, BaseSettings, Config


class Plugin(BasePlugin[BaseSettings]):
    config = Config(
        name="filebrowser",
        descriptive_name="File Browser",
        version="0.1.0",
        description="File Browser as a Lungo plugin.",
        have_backend=True,
        require_account=True,
        web_icon="icons/FolderOutline.svelte",
        web_alt_icon="icons/FolderSolid.svelte",
    )
