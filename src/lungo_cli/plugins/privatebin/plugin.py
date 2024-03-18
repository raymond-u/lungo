from typing import override

from lungo_cli.core.plugin import BasePlugin, Config


class Plugin(BasePlugin):
    config = Config(
        name="privatebin",
        descriptive_name="PrivateBin",
        version="0.1.0",
        description="PrivateBin as a Lungo plugin.",
        have_backend=True,
        require_account=False,
        web_icon="icons/NoteOutline.svelte",
        web_alt_icon="icons/NoteSolid.svelte",
    )

    @override
    def update_data(self) -> None:
        # Allow the non-root container user to write
        self.file_utils.change_mode(self.storage.managed_dir / "privatebin", 0o777)
