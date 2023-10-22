from os import PathLike
from pathlib import Path

from importlib_resources import as_file, files
from typer import Exit

from .console import Console
from .constants import PACKAGE_NAME
from .context import ContextManager
from .database import AccountManager
from .file import FileUtils
from .renderer import Renderer
from .storage import Storage
from ..helpers.common import format_path, get_file_permissions
from ..helpers.crypto import generate_random_hex, generate_self_signed_cert
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

    def process_args_delayed(self, dev: bool, force_init: bool = False, remove_lock: bool = False) -> None:
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

    def ensure_application_data(self) -> None:
        """Ensure that all the application data exists and is up-to-date."""
        with self.console.status("Updating storage..."):
            self.storage.validate()
            self.storage.create_dirs()

            if not self.storage.bundled_dir.is_dir() or self.context_manager.dev:
                self.console.print_info("Updating bundled data...")
                self.copy_app_resources(".", self.storage.bundled_dir)
                self.file_utils.change_mode(self.storage.bundled_dir, 0o700)
                self.file_utils.remove(self.storage.init_file)

            if not self.storage.nginx_cert_file.is_file() or not self.storage.nginx_key_file.is_file():
                self.console.print_info("Generating self-signed certificate...")
                cert, key = generate_self_signed_cert()
                self.file_utils.write_bytes(self.storage.nginx_cert_file, cert)
                self.file_utils.write_bytes(self.storage.nginx_key_file, key, True)

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
                self.account_manager.verify(self.context_manager.config, self.context_manager.users)
                self.account_manager.update(self.context_manager.config, self.context_manager.users)

                self.file_utils.write_text(self.storage.init_file, config_hash)

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

        self.context_manager.config = config
        self.context_manager.users = users
