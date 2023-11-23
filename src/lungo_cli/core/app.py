import os
from os import PathLike
from pathlib import Path
from uuid import uuid1

from importlib_resources import as_file, files
from typer import Exit

from .console import Console
from .constants import PACKAGE_NAME
from .context import ContextManager
from .database import AccountManager
from .file import FileUtils
from .renderer import Renderer
from .storage import Storage
from ..helpers.common import get_file_permissions, port_is_available
from ..helpers.crypto import generate_random_hex, generate_self_signed_cert
from ..helpers.format import format_input, format_path
from ..models.base import EApp
from ..models.config import Config
from ..models.users import Users


class AppManager:
    def __init__(
        self,
        console: Console,
        file_utils: FileUtils,
        storage: Storage,
        context_manager: ContextManager,
        account_manager: AccountManager,
        renderer: Renderer,
    ):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self.context_manager = context_manager
        self.account_manager = account_manager
        self.renderer = renderer

    def process_args(self, config_dir: str | PathLike[str] | None, quiet: bool, verbosity: int) -> None:
        """Process common arguments."""
        if config_dir:
            if not Path(config_dir).is_dir():
                self.console.print_error(f"{format_path(config_dir)} is not a directory.")
                raise Exit(code=1)

            self.storage.config_dir = Path(config_dir).resolve()

        if quiet:
            self.console.set_log_level(-1)
        else:
            self.console.set_log_level(verbosity)

    def process_args_deferred(self, dev: bool, force_init: bool = False, remove_lock: bool = False) -> None:
        """Process common arguments that need to be processed after the configuration is loaded."""
        if dev:
            self.console.set_log_level(1)
            self.storage.storage_version = "dev"
            self.context_manager.dev = True

        if force_init:
            self.file_utils.remove(self.storage.bundled_dir)

        if remove_lock:
            self.file_utils.remove(self.storage.lock_file)

    def copy_app_resources(self, src: str | PathLike[str], dst: str | PathLike[str]) -> None:
        """Copy resources from the package to the destination directory."""
        with as_file(files(f"{PACKAGE_NAME}.resources")) as resources:
            self.file_utils.copy(resources / src, dst)

    def update_app_data(self) -> None:
        """Ensure that all the application data exists and is up-to-date."""
        with self.console.status("Updating storage..."):
            self.storage.validate()
            self.storage.create_dirs()

            if not self.storage.bundled_dir.is_dir() or self.context_manager.dev:
                self.console.print_info("Updating bundled data...")
                self.copy_app_resources(".", self.storage.bundled_dir)
                self.file_utils.change_mode(self.storage.bundled_dir, 0o700)
                self.file_utils.remove(self.storage.init_file)

            if not self.storage.nginx_gateway_cert_file.is_file() or not self.storage.nginx_gateway_key_file.is_file():
                self.console.print_info("Generating self-signed certificate...")
                cert, key = generate_self_signed_cert()
                self.file_utils.write_bytes(self.storage.nginx_gateway_cert_file, cert)
                self.file_utils.write_bytes(self.storage.nginx_gateway_key_file, key, True)

            if not self.storage.kratos_secrets_file.is_file():
                self.console.print_info("Generating Kratos secrets...")
                self.renderer.render(
                    self.storage.template_kratos_secrets_rel,
                    self.storage.kratos_secrets_file,
                    secret_cookie=generate_random_hex(),
                )
                self.file_utils.change_mode(self.storage.kratos_secrets_file, 0o600)

            if not self.storage.jupyterhub_cookie_secret_file.is_file():
                self.console.print_info("Generating JupyterHub cookie secret...")
                self.file_utils.write_text(self.storage.jupyterhub_cookie_secret_file, generate_random_hex(), True)

            if not self.storage.jupyterhub_password_file.is_file():
                self.console.print_info("Generating JupyterHub password...")
                self.file_utils.write_text(self.storage.jupyterhub_password_file, generate_random_hex(), True)

            if not self.storage.rstudio_password_file.is_file():
                self.console.print_info("Generating RStudio password...")
                self.file_utils.write_text(self.storage.rstudio_password_file, generate_random_hex(), True)

            if not self.storage.xray_salt_file.is_file():
                self.console.print_info("Generating Xray salt...")
                self.file_utils.write_text(self.storage.xray_salt_file, str(uuid1()), True)

        with self.console.status("Updating database..."):
            config_hash = self.file_utils.hash_sha256(self.storage.config_file) + self.file_utils.hash_sha256(
                self.storage.users_file
            )

            if (
                not self.storage.init_file.is_file()
                or self.file_utils.read_text(self.storage.init_file) != config_hash
                or self.context_manager.dev
            ):
                self.file_utils.remove(self.storage.init_file)

                self.renderer.render_all(self.context_manager.context)
                self.account_manager.update(self.context_manager.config, self.context_manager.users)

                self.file_utils.write_text(self.storage.init_file, config_hash)

    def ensure_port_availability(self) -> None:
        """Ensure that ports used by the application are available."""
        if self.context_manager.config.network.http.enabled and not port_is_available(
            self.context_manager.config.network.http.port
        ):
            self.console.print_error(f"Port {format_input(self.context_manager.config.network.http.port)} is in use.")
            raise Exit(code=1)

        if not port_is_available(self.context_manager.config.network.https.port):
            self.console.print_error(f"Port {format_input(self.context_manager.config.network.https.port)} is in use.")
            raise Exit(code=1)

    def load_config(self) -> None:
        """Load the configuration files into the context manager."""
        files_missing = False

        if not self.storage.config_file.is_file():
            self.console.print_error(
                f"{format_path(self.storage.config_file.name)} not found. "
                "A template will be created, please read the manual to learn how to configure it."
            )
            self.copy_app_resources(self.storage.template_config_rel, self.storage.config_file)
            files_missing = True

        if not self.storage.users_file.is_file():
            self.console.print_error(
                f"{format_path(self.storage.users_file.name)} not found. "
                "A template will be created, please read the manual to learn how to configure it."
            )
            self.copy_app_resources(self.storage.template_users_rel, self.storage.users_file)
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

        config = self.file_utils.parse_yaml(self.storage.config_file, Config)
        users = self.file_utils.parse_yaml(self.storage.users_file, Users)

        if config.directories.cache_dir:
            self.storage.cache_dir = config.directories.cache_dir.resolve()
        if config.directories.data_dir:
            self.storage.data_dir = config.directories.data_dir.resolve()

        self.verify_config(config, users)

        self.context_manager.config = config
        self.context_manager.users = users

    def verify_config(self, config: Config, users: Users) -> None:
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
                # Pydantic does not distinguish between a string and a enum value
                if type(allowed_app) is str:
                    allowed_app = EApp(allowed_app)

                if allowed_app in (EApp.FILEBROWSER, EApp.JUPYTERHUB, EApp.RSTUDIO):
                    self.console.print_error(
                        "An anonymous account is required when the unregistered role "
                        "has access to applications that require an account."
                    )
                    raise Exit(code=1)
