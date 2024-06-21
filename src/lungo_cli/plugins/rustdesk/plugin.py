import base64
from pathlib import Path
from typing import Any, override

from lungo_cli.core.plugin import BasePlugin, BaseSettings, PluginManifest
from lungo_cli.helpers.crypto import generate_raw_ed25519_keypair


class Plugin(BasePlugin[BaseSettings]):
    manifest = PluginManifest(
        name="rustdesk",
        version="0.2.0",
        descriptive_name="RustDesk",
        description="RustDesk as a Lungo plugin.",
        compatible_with="~=0.5.0",
        have_backend=True,
        backend_host_ports=[21115, 21116, 21117],
        require_account=False,
        web_icon="icons/Rustdesk.svelte",
    )

    @property
    def private_key_file(self) -> Path:
        return self.storage.generated_dir / self.manifest.name / "id_ed25519"

    @property
    def public_key_file(self) -> Path:
        return self.storage.generated_dir / self.manifest.name / "id_ed25519.pub"

    @override
    def get_custom_rendering_context(self) -> dict[str, Any]:
        return {
            "rustdesk_private_key": self.file_utils.read_text(self.private_key_file),
            "rustdesk_public_key": self.file_utils.read_text(self.public_key_file),
            "rustdesk_server_version": "1.1.11-1",
        }

    @override
    def on_plugin_initialization(self) -> None:
        if not self.private_key_file.is_file() or not self.public_key_file.is_file():
            self.console.print_info("Generating RustDesk keypair...")

            public_key, private_key = generate_raw_ed25519_keypair()
            private_key_b64 = base64.b64encode(private_key + public_key).decode()
            public_key_b64 = base64.b64encode(public_key).decode()

            self.file_utils.write_text(self.private_key_file, private_key_b64, True)
            self.file_utils.write_text(self.public_key_file, public_key_b64, True)
