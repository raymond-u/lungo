from ipaddress import IPv4Network
from pathlib import Path
from typing import Any, override, Type
from uuid import UUID, uuid1, uuid5

from lungo_cli.core.plugin import BasePlugin, BaseSettings, Config


class Settings(BaseSettings):
    domain_whitelist: list[str] = []
    domain_keyword_whitelist: list[str] = []
    domain_suffix_whitelist: list[str] = []
    ip_range_whitelist: list[IPv4Network] = []


class Plugin(BasePlugin):
    config = Config(
        name="xray",
        descriptive_name="Xray",
        version="0.1.0",
        description="Xray as a Lungo plugin.",
        have_backend=True,
        require_account=True,
        web_icon="ProxyOutline.svelte",
        web_alt_icon="ProxySolid.svelte",
    )

    @property
    def salt_file(self) -> Path:
        return self.storage.generated_dir / "xray" / "salt"

    @classmethod
    @override
    def get_plugin_settings_cls(cls) -> Type[BaseSettings]:
        return Settings

    @override
    def get_render_context(self) -> dict[str, Any]:
        salt = UUID(self.file_utils.read_text(self.salt_file))

        return {
            "xray_accounts": [
                (account.email, uuid5(salt, account.username)) for account in self.context_manager.users.accounts
            ],
            "xray_salt": salt,
        }

    @override
    def update_data(self) -> None:
        if not self.salt_file.is_file():
            self.console.print_info("Generating Xray salt...")
            self.file_utils.write_text(self.salt_file, str(uuid1()), True)
