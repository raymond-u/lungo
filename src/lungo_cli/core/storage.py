import os
from os import PathLike
from pathlib import Path

from platformdirs import user_cache_path, user_config_path, user_data_path

from .console import Console
from .constants import APP_AUTHOR, APP_NAME, STORAGE_PREFIX, STORAGE_VERSION
from .file import FileUtils
from ..helpers.format import format_path
from ..models.base import EService


class Storage:
    """Contain all the paths used by the application."""

    def __init__(self, console: Console, file_utils: FileUtils):
        self.console = console
        self.file_utils = file_utils
        self._storage_version = STORAGE_VERSION
        self._cache_dir = user_cache_path(APP_NAME, APP_AUTHOR)
        self._config_dir = user_config_path(APP_NAME, APP_AUTHOR)
        self._data_dir = user_data_path(APP_NAME, APP_AUTHOR)

    @property
    def storage_version(self) -> str:
        return self._storage_version

    @storage_version.setter
    def storage_version(self, value: str):
        self._storage_version = value

    @property
    def config_dir(self) -> Path:
        return self._config_dir

    @config_dir.setter
    def config_dir(self, value: str | PathLike[str]):
        self._config_dir = Path(value)

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    @cache_dir.setter
    def cache_dir(self, value: str | PathLike[str]):
        self._cache_dir = Path(value)

    @property
    def cache_latest_dir(self) -> Path:
        return self._cache_dir / self._storage_version

    @property
    def data_dir(self) -> Path:
        return self._data_dir

    @data_dir.setter
    def data_dir(self, value: str | PathLike[str]):
        self._data_dir = Path(value)

    @property
    def data_latest_dir(self) -> Path:
        return self._data_dir / self._storage_version

    @property
    def bundled_dir(self) -> Path:
        return self.data_latest_dir / self.bundled_rel

    @property
    def bundled_rel(self) -> Path:
        return Path("bundled")

    @property
    def generated_dir(self) -> Path:
        return self.data_latest_dir / self.generated_rel

    @property
    def generated_rel(self) -> Path:
        return Path("generated")

    @property
    def managed_dir(self) -> Path:
        return self.data_latest_dir / self.managed_rel

    @property
    def managed_rel(self) -> Path:
        return Path("managed")

    @property
    def excluded_rel(self) -> Path:
        return Path("excluded")

    @property
    def config_file(self) -> Path:
        return self._config_dir / "config.yaml"

    @property
    def users_file(self) -> Path:
        return self._config_dir / "users.yaml"

    @property
    def init_file(self) -> Path:
        return self.data_latest_dir / ".init"

    @property
    def lock_file(self) -> Path:
        return self.data_latest_dir / ".lock"

    @property
    def service_keto_admin_dir(self) -> Path:
        return self.bundled_dir / "dockerfiles" / "keto_admin"

    @property
    def service_kratos_admin_dir(self) -> Path:
        return self.bundled_dir / "dockerfiles" / "kratos_admin"

    @property
    def template_config_rel(self) -> Path:
        return self.excluded_rel / "config.yaml"

    @property
    def template_users_rel(self) -> Path:
        return self.excluded_rel / "users.yaml"

    @property
    def template_kratos_secrets_rel(self) -> Path:
        return self.excluded_rel / "kratos" / "secrets.yaml.jinja"

    @property
    def nginx_gateway_cert_file(self) -> Path:
        return self.generated_dir / "nginx_gateway" / "lungo.crt"

    @property
    def nginx_gateway_key_file(self) -> Path:
        return self.generated_dir / "nginx_gateway" / "lungo.key"

    @property
    def kratos_secrets_file(self) -> Path:
        return self.generated_dir / "kratos" / "secrets.yaml"

    @property
    def jupyterhub_cookie_secret_file(self) -> Path:
        return self.generated_dir / "jupyterhub" / "cookie_secret"

    @property
    def jupyterhub_password_file(self) -> Path:
        return self.generated_dir / "jupyterhub" / "password"

    @property
    def rstudio_password_file(self) -> Path:
        return self.generated_dir / "rstudio" / "password"

    @property
    def xray_salt_file(self) -> Path:
        return self.generated_dir / "xray" / "salt"

    def validate(self) -> None:
        if self.data_latest_dir.is_dir():
            return

        largest_version = -1

        # List all directories in the data directory
        for dir_ in self.data_dir.glob(f"{STORAGE_PREFIX}*{os.sep}"):
            if (version := dir_.name.split(STORAGE_PREFIX, 1)[1]).isdigit():
                version_number = int(version)

                if version_number > largest_version:
                    largest_version = version_number

        if largest_version >= 0:
            self.migrate(self.data_dir / f"{STORAGE_PREFIX}{largest_version}")

    def migrate(self, from_: str | PathLike[str]) -> None:
        self.console.print_info(f"Migrating storage from {format_path(Path(from_).name)}...")

        self.file_utils.copy(from_ / self.generated_rel, self.generated_dir)
        self.file_utils.copy(from_ / self.managed_rel, self.managed_dir)

    def create_dirs(self) -> None:
        app: EService
        for app in EService:
            self.file_utils.create_dir(self.cache_latest_dir / app.value)
            self.file_utils.change_mode(self.cache_latest_dir / app.value, 0o700)
            self.file_utils.create_dir(self.managed_dir / app.value)
            self.file_utils.change_mode(self.managed_dir / app.value, 0o700)

        # Allow the non-root container user to write
        self.file_utils.change_mode(self.managed_dir / EService.PRIVATEBIN.value, 0o777)
