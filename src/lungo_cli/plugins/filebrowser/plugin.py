from lungo_cli.core.plugin import BasePlugin, Config


class Plugin(BasePlugin):
    config = Config(
        name="filebrowser",
        descriptive_name="File Browser",
        version="0.1.0",
        description="File Browser as a Lungo plugin.",
        have_backend=True,
        require_account=True,
        web_icon="FolderOutline.svelte",
        web_alt_icon="FolderSolid.svelte",
    )
