from pathlib import Path
from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginConfig
from lungo_cli.helpers.crypto import generate_random_hex


class Settings(BaseSettings):
    password: str | None = None


class Plugin(BasePlugin[Settings]):
    config = PluginConfig(
        name="jupyterhub",
        descriptive_name="JupyterHub",
        version="0.1.0",
        description="JupyterHub as a Lungo plugin.",
        compatible_with="~=0.3.0",
        have_backend=True,
        require_account=True,
        web_icon="icons/Jupyter.svelte",
    )

    @property
    def cookie_secret_file(self) -> Path:
        return self.storage.generated_dir / "jupyterhub" / "cookie_secret"

    @property
    def password_file(self) -> Path:
        return self.storage.generated_dir / "jupyterhub" / "password"

    @classmethod
    @override
    def get_plugin_settings_cls(cls) -> type[Settings]:
        return Settings

    @override
    def get_render_context(self) -> dict[str, Any]:
        return {"jupyterhub_password": self.settings.password or self.file_utils.read_text(self.password_file)}

    @override
    def update_data(self) -> None:
        if not self.cookie_secret_file.is_file():
            self.console.print_info("Generating JupyterHub cookie secret...")
            self.file_utils.write_text(self.cookie_secret_file, generate_random_hex(), True)

        if not self.password_file.is_file():
            self.console.print_info("Generating JupyterHub password...")
            self.file_utils.write_text(self.password_file, generate_random_hex(), True)
