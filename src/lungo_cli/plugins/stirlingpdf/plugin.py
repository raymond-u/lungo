from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="stirlingpdf",
        version="0.1.0",
        descriptive_name="Stirling PDF",
        description="Stirling PDF as a Lungo plugin.",
        compatible_with="~=0.3.0",
        have_backend=True,
        backend_port=8080,
        require_account=False,
        web_icon="icons/StirlingPdf.svelte",
    )

    @override
    def get_render_context(self) -> dict[str, Any]:
        return {"stirlingpdf_version": "0.22.8"}
