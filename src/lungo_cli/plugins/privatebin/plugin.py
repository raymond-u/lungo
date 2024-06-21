from pathlib import Path
from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="privatebin",
        version="0.3.0",
        descriptive_name="Pastebin",
        description="PrivateBin as a Lungo plugin.",
        compatible_with="~=0.5.0",
        have_backend=True,
        backend_port=80,
        require_account=False,
        web_icon="icons/NoteOutline.svelte",
        web_alt_icon="icons/NoteSolid.svelte",
    )

    @property
    def data_dir(self) -> Path:
        return self.storage.managed_dir / self.manifest.name / "data"

    @override
    def get_custom_rendering_context(self) -> dict[str, Any]:
        return {"privatebin_version": "1.7.3"}

    @override
    def on_plugin_initialization(self) -> None:
        # Allow the non-root container user to write
        self.file_utils.create_dir(self.data_dir)
        self.file_utils.change_mode(self.data_dir, 0o777)
