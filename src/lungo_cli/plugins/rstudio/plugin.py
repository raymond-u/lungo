from pathlib import Path
from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest
from lungo_cli.helpers.crypto import generate_random_hex


class Settings(BaseSettings):
    password: str | None = None


class Plugin(BasePlugin[Settings]):
    manifest = PluginManifest(
        name="rstudio",
        version="0.3.0",
        descriptive_name="RStudio",
        description="RStudio as a Lungo plugin.",
        compatible_with="~=0.5.0",
        have_backend=True,
        backend_port=80,
        require_account=True,
        web_icon="icons/RStudioOutline.svelte",
        web_alt_icon="icons/RStudioSolid.svelte",
    )

    @property
    def password_file(self) -> Path:
        return self.storage.generated_dir / self.manifest.name / "password"

    @classmethod
    @override
    def get_plugin_settings_cls(cls) -> type[Settings]:
        return Settings

    @override
    def get_custom_rendering_context(self) -> dict[str, Any]:
        return {
            "rstudio_password": self.settings.password or self.file_utils.read_text(self.password_file),
            "rstudio_version": "4.4.1",
        }

    @override
    def on_plugin_initialization(self) -> None:
        if not self.password_file.is_file():
            self.console.print_info("Generating RStudio password...")
            self.file_utils.write_text(self.password_file, generate_random_hex(), True)
