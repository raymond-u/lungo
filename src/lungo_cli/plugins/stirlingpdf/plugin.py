from pathlib import Path
from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="stirlingpdf",
        version="0.2.0",
        descriptive_name="Stirling PDF",
        description="Stirling PDF as a Lungo plugin.",
        compatible_with="~=0.5.0",
        have_backend=True,
        backend_port=8080,
        require_account=False,
        web_icon="icons/StirlingPdf.svelte",
    )

    @property
    def logs_dir(self) -> Path:
        return self.storage.cache_latest_dir / self.manifest.name / "logs"

    @override
    def get_custom_rendering_context(self) -> dict[str, Any]:
        return {"stirlingpdf_version": "0.26.1"}

    @override
    def on_plugin_initialization(self) -> None:
        self.file_utils.create_dir(self.logs_dir)
