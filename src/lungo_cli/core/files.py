from pathlib import Path
from typing import Generator

from platformdirs import user_cache_path, user_config_path, user_data_path

from .constants import APP_AUTHOR, APP_NAME


class AppFiles:
    """A class for managing the application's files."""

    def __init__(self):
        self._cache_dir = user_cache_path(APP_NAME, APP_AUTHOR)
        self._config_dir = user_config_path(APP_NAME, APP_AUTHOR)
        self._data_dir = user_data_path(APP_NAME, APP_AUTHOR)

    @property
    def all_directories(self) -> Generator[Path]:
        dirs = [self.cache_dir, self.config_dir, self.data_dir]
        apps = ["authelia", "filebrowser", "nginx", "rstudio"]
        return (dir_ / app for dir_ in dirs for app in apps)

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    @property
    def config_dir(self) -> Path:
        return self._config_dir

    @property
    def data_dir(self) -> Path:
        return self._data_dir

    @property
    def compose_dir(self) -> Path:
        return self._config_dir

    @property
    def authelia_env(self) -> Path:
        return self.config_dir / "authelia" / "authelia.env"

    @property
    def authelia_smtp_password(self) -> Path:
        return self.config_dir / "authelia" / "notifier_smtp_password"

    @property
    def authelia_db(self) -> Path:
        return self.data_dir / "authelia" / "authelia.sqlite3"

    @property
    def authelia_encryption_key(self) -> Path:
        return self.data_dir / "authelia" / "storage_encryption_key"

    @property
    def authelia_jwt_secret(self) -> Path:
        return self.data_dir / "authelia" / "jwt_secret"

    @property
    def authelia_users(self) -> Path:
        return self.data_dir / "authelia" / "users.yaml"

    @property
    def filebrowser_dockerfile(self) -> Path:
        return self.config_dir / "filebrowser" / "Dockerfile"

    @property
    def filebrowser_users(self) -> Path:
        return self.data_dir / "filebrowser" / "users_export.yaml"

    @property
    def nginx_cert(self) -> Path:
        return self.data_dir / "nginx" / "cert.pem"

    @property
    def nginx_key(self) -> Path:
        return self.data_dir / "nginx" / "key.pem"

    @property
    def rstudio_dockerfile(self) -> Path:
        return self.config_dir / "rstudio" / "Dockerfile"
