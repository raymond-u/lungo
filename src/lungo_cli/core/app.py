import os
from os import PathLike
from pathlib import Path

from typer import Exit

from .console import Console
from .constants import PACKAGE_NAME
from .context import ContextManager
from .database import AccountManager
from .file import FileUtils
from .plugin import PluginManager
from .renderer import Renderer
from .storage import Storage
from ..helpers.common import get_app_version, get_file_permissions
from ..helpers.crypto import generate_random_hex, generate_self_signed_cert, hash_text
from ..helpers.format import format_input, format_path
from ..models.base import EApp
from ..models.config import Config, CoreConfig
from ..models.users import Users


class AppManager:
    """Manager for the application."""

    def __init__(
        self,
        account_manager: AccountManager,
        console: Console,
        context_manager: ContextManager,
        file_utils: FileUtils,
        plugin_manager: PluginManager,
        renderer: Renderer,
        storage: Storage,
    ):
        self.account_manager = account_manager
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.plugin_manager = plugin_manager
        self.renderer = renderer
        self.storage = storage

        self.force_init = False

    def process_cli_options(
        self, config_dir: str | PathLike[str] | None, dev: bool, quiet: bool, verbosity: int, force_init: bool = False
    ) -> None:
        """Process common arguments."""
        if config_dir:
            if not Path(config_dir).is_dir():
                self.console.print_error(f"{format_path(config_dir)} is not a directory.")
                raise Exit(code=1)

            self.storage.config_dir = Path(config_dir).resolve()

        if dev:
            self.console.set_log_level(1)
            self.storage.storage_version = "dev"
            self.context_manager.dev = True
            self.force_init = True

        if quiet:
            self.console.set_log_level(-1)
        else:
            self.console.set_log_level(verbosity)

        if force_init:
            self.force_init = True

    def load_core_config(self) -> None:
        """Load the core part of the configuration file that is critical to set up the application."""
        files_missing = False

        if not self.storage.config_file.is_file():
            self.console.print_error(
                f"{format_path(self.storage.config_file.name)} not found. "
                "A template has been created in place of the missing file."
            )
            self.file_utils.copy_package_resources(
                f"{PACKAGE_NAME}.resources",
                self.storage.template_config_rel,
                self.storage.config_file,
            )
            files_missing = True

        if not self.storage.users_file.is_file():
            self.console.print_error(
                f"{format_path(self.storage.users_file.name)} not found. "
                "A template has been created in place of the missing file."
            )
            self.file_utils.copy_package_resources(
                f"{PACKAGE_NAME}.resources",
                self.storage.template_users_rel,
                self.storage.users_file,
            )
            files_missing = True

        if files_missing:
            raise Exit(code=1)

        if (permission := get_file_permissions(self.storage.config_file))[1:] != "00":
            self.console.print_warning(
                f"{format_path(self.storage.config_file)} should not be readable or writable by other users "
                f"(recommended permission: 600, current permission: {permission})."
            )
        if (permission := get_file_permissions(self.storage.users_file))[1:] != "00":
            self.console.print_warning(
                f"{format_path(self.storage.users_file)} should not be readable or writable by other users "
                f"(recommended permission: 600, current permission: {permission})."
            )

        core_config = self.file_utils.parse_yaml(self.storage.config_file, CoreConfig)

        if core_config.directories.cache_dir:
            self.storage.cache_dir = core_config.directories.cache_dir.resolve()
        if core_config.directories.data_dir:
            self.storage.data_dir = core_config.directories.data_dir.resolve()

    def load_full_config(self) -> None:
        """Load the full configuration files into the context manager."""
        self.load_core_config()
        self.plugin_manager.extend_models()

        config = self.file_utils.parse_yaml(self.storage.config_file, Config)
        users = self.file_utils.parse_yaml(self.storage.users_file, Users)

        self.verify_config(config, users)

        self.context_manager.config = config
        self.context_manager.users = users

    def verify_config(self, config: Config, users: Users) -> None:
        """Verify the configuration files."""
        shared_dirs = list(map(lambda x: x.name, config.directories.shared_dirs))
        anonymous_account_exists = False

        for account in users.accounts:
            if account.username == "anonymous":
                self.console.print_info(
                    f"Found username {format_input('anonymous')}. "
                    "This user will serve as a shared account for anonymous access."
                )
                anonymous_account_exists = True

            if not (path := (account.extra.user_dir or config.directories.users_dir / account.username)).is_dir():
                if os.access(path.parent, os.W_OK):
                    self.console.print_info(f"Creating user directory at {format_path(path)}...")
                    self.file_utils.create_dir(path)
                else:
                    self.console.print_error(
                        f"User directory at {format_path(path)} does not exist. "
                        "Please create it with the appropriate permissions."
                    )
                    raise Exit(code=1)

            shared_dirs.extend(map(lambda x: x.name, account.extra.shared_dirs))

        if len(shared_dirs) != len(set(shared_dirs)):
            self.console.print_error("Duplicate shared directories detected. Please use unique directory names.")
            raise Exit(code=1)

        if not anonymous_account_exists:
            if config.rules.privileges.unregistered.allowed_apps == "all":
                self.console.print_error(
                    "An anonymous account is required when the unregistered role has access to all applications."
                )
                raise Exit(code=1)

            for allowed_app in config.rules.privileges.unregistered.allowed_apps:
                # Pydantic does not distinguish between a string and an enum value
                if type(allowed_app) is EApp:
                    allowed_app = allowed_app.value

                if next(
                    (
                        plugin_cls.config.require_account
                        for plugin_cls in self.plugin_manager.compatible_plugin_classes
                        if plugin_cls.config.name == allowed_app
                    ),
                    False,
                ):
                    self.console.print_error(
                        "An anonymous account is required when the unregistered role "
                        "has access to applications that require an account."
                    )
                    raise Exit(code=1)

    def generate_config_hash(self) -> str:
        """Generate a hash of the configuration files."""
        ordered_plugins = sorted(self.plugin_manager.compatible_plugin_classes, key=lambda x: x.config.name)

        return hash_text(
            "+".join(
                [
                    f"v{get_app_version()}",
                    *(
                        map(
                            lambda x: f"{x.config.name}{f'v{x.config.version}' if x.config.version else ''}",
                            ordered_plugins,
                        )
                    ),
                    self.file_utils.hash_sha256(self.storage.config_file),
                    self.file_utils.hash_sha256(self.storage.users_file),
                ]
            )
        )

    def update_app_data(self) -> None:
        """Ensure that all the application data exists and is up-to-date."""
        config_hash = self.generate_config_hash()

        with self.console.status("Updating app data..."):
            self.storage.validate()

            if (
                self.force_init
                or not self.storage.bundled_dir.is_dir()
                or not self.storage.init_file.is_file()
                or self.file_utils.read_text(self.storage.init_file) != config_hash
            ):
                self.console.print_info("Updating bundled resources...")

                # Backup the installed plugins directory if it exists
                if self.storage.installed_plugins_dir.is_dir():
                    self.file_utils.move(self.storage.installed_plugins_dir, self.storage.cache_plugins_dir)

                self.file_utils.copy_package_resources(f"{PACKAGE_NAME}.resources", ".", self.storage.bundled_dir)

                if self.storage.cache_plugins_dir.is_dir():
                    self.file_utils.move(self.storage.cache_plugins_dir, self.storage.installed_plugins_dir)

                self.file_utils.change_mode(self.storage.bundled_dir, 0o700)
                self.file_utils.remove(self.storage.init_file)

            if not self.storage.nginx_gateway_cert_file.is_file() or not self.storage.nginx_gateway_key_file.is_file():
                self.console.print_info("Generating self-signed certificate...")
                cert, key = generate_self_signed_cert()
                self.file_utils.write_bytes(self.storage.nginx_gateway_cert_file, cert)
                self.file_utils.write_bytes(self.storage.nginx_gateway_key_file, key, True)

            # Remove the socket file every time to avoid binding issues
            self.file_utils.remove(self.storage.nginx_gateway_socket_file)

            if not self.storage.kratos_secrets_file.is_file():
                self.console.print_info("Generating Kratos secrets...")
                self.renderer.render(
                    self.storage.template_kratos_secrets_rel,
                    self.storage.kratos_secrets_file,
                    secret_cookie=generate_random_hex(),
                )
                self.file_utils.change_mode(self.storage.kratos_secrets_file, 0o600)

            self.plugin_manager.initialize_plugins()

            if not self.storage.init_file.is_file():
                for plugin in self.plugin_manager.plugins:
                    self.renderer.render_plugin(plugin)
                    self.context_manager.plugin_outputs.append(plugin.output)

                self.renderer.render_main()
                self.account_manager.update(self.context_manager.config, self.context_manager.users)

                # Delay copying the web files until the templates have all been rendered
                for plugin in self.plugin_manager.plugins:
                    for web_dir in (self.storage.installed_plugins_dir / plugin.config.name / "web").iterdir():
                        if web_dir.name == "lib":
                            dst_prefix = self.storage.bundled_dir / "web" / "src" / "lib" / "plugins"
                            self.file_utils.copy(web_dir, dst_prefix / plugin.config.name)
                        elif web_dir.name == "routes":
                            dst_prefix = self.storage.bundled_dir / "web" / "src" / "routes" / "(apps)" / "app"
                            self.file_utils.copy(web_dir, dst_prefix / plugin.config.name)

                if self.context_manager.config.branding.cover:
                    self.file_utils.copy(
                        self.context_manager.config.branding.cover,
                        self.storage.bundled_dir / "web" / "src" / "lib" / "assets" / "cover.jpg",
                    )

                if self.context_manager.config.branding.logo:
                    self.file_utils.copy(
                        self.context_manager.config.branding.logo,
                        self.storage.bundled_dir / "web" / "static" / "favicon.png",
                    )

                self.file_utils.write_text(self.storage.init_file, config_hash)
