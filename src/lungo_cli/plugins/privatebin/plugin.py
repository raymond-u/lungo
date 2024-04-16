from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="privatebin",
        version="0.1.0",
        descriptive_name="Pastebin",
        description="PrivateBin as a Lungo plugin.",
        compatible_with="~=0.3.0",
        have_backend=True,
        backend_port=80,
        require_account=False,
        web_icon="icons/NoteOutline.svelte",
        web_alt_icon="icons/NoteSolid.svelte",
    )

    @override
    def get_render_context(self) -> dict[str, Any]:
        return {"privatebin_version": "1.7.1"}

    @override
    def update_data(self) -> None:
        # Allow the non-root container user to write
        self.file_utils.change_mode(self.storage.managed_dir / self.manifest.name, 0o777)
