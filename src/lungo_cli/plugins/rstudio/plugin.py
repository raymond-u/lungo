from pathlib import Path
from typing import Any, override, Type

from lungo_cli.core.plugin import BasePlugin, BaseSettings, Config
from lungo_cli.helpers.crypto import generate_random_hex


class Settings(BaseSettings):
    password: str | None = None


class Plugin(BasePlugin):
    config = Config(
        name="rstudio",
        descriptive_name="RStudio",
        version="0.1.0",
        description="RStudio as a Lungo plugin.",
        have_backend=True,
        require_account=True,
        web_icon="RStudioOutline.svelte",
        web_alt_icon="RStudioSolid.svelte",
    )

    @property
    def password_file(self) -> Path:
        return self.storage.generated_dir / "rstudio" / "password"

    @classmethod
    @override
    def get_plugin_settings_cls(cls) -> Type[BaseSettings]:
        return Settings

    @override
    def get_render_context(self) -> dict[str, Any]:
        return {"rstudio_password": self.settings.password or self.file_utils.read_text(self.password_file)}

    @override
    def update_data(self) -> None:
        if not self.password_file.is_file():
            self.console.print_info("Generating RStudio password...")
            self.file_utils.write_text(self.password_file, generate_random_hex(), True)
