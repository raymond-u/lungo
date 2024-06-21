import socket
from ipaddress import IPv4Address

from typer import Exit

from .console import Console
from .constants import (
    APP_NAME,
    APP_NAME_CAPITALIZED,
    ARCHITECTURE,
    KETO_VERSION,
    KRATOS_VERSION,
    NODE_VERSION,
    OATHKEEPER_VERSION,
    OPENRESTY_VERSION,
    PACKAGE_NAME,
)
from .file import FileUtils
from .storage import Storage
from ..helpers.format import format_input
from ..models.base import AppDirs, EApp, ECoreService
from ..models.config import Config
from ..models.context import Constants, Context
from ..models.plugin import PluginOutput
from ..models.users import Users


class ContextManager:
    """Manage the context of the application, can be passed to the renderer to render templates."""

    def __init__(self, console: Console, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage

        self._config = None
        self._users = None
        self._plugin_outputs = []
        self._dev = False
        self._local_ip = None

    @property
    def constants(self) -> Constants:
        return Constants(
            app_name=APP_NAME,
            app_name_capitalized=APP_NAME_CAPITALIZED,
            architecture=ARCHITECTURE,
            package_name=PACKAGE_NAME,
            openresty_version=OPENRESTY_VERSION,
            keto_version=KETO_VERSION,
            kratos_version=KRATOS_VERSION,
            oathkeeper_version=OATHKEEPER_VERSION,
            node_version=NODE_VERSION,
        )

    @property
    def config(self) -> Config:
        if self._config is None:
            self.console.print_error("Config is not set.")
            raise Exit(code=1)

        return self._config

    @config.setter
    def config(self, value: Config):
        self._config = value

    @property
    def users(self) -> Users:
        if self._users is None:
            self.console.print_error("Users are not set.")
            raise Exit(code=1)

        return self._users

    @users.setter
    def users(self, value: Users):
        self._users = value

    @property
    def plugin_outputs(self) -> list[PluginOutput]:
        return self._plugin_outputs

    @plugin_outputs.setter
    def plugin_outputs(self, value: list[PluginOutput]):
        self._plugin_outputs = value

    @property
    def app_dirs(self) -> AppDirs:
        return AppDirs(
            cache_dir=str(self.storage.cache_latest_dir),
            generated_dir=str(self.storage.generated_dir),
            managed_dir=str(self.storage.managed_dir),
            plugin_dir=str(self.storage.plugins_rel),
        )

    @property
    def dev(self) -> bool:
        return self._dev

    @dev.setter
    def dev(self, value: bool):
        self._dev = value

    @property
    def ip_addresses(self) -> dict[str, IPv4Address]:
        if self.config.network.subnet.num_addresses < 256:
            self.console.print_error(
                f"Subnet {format_input(str(self.config.network.subnet))} is too small. "
                "Please change it to a subnet with at least 256 addresses."
            )
            raise Exit(code=1)

        hosts = list(self.config.network.subnet.hosts())

        # Reserve the first 16 addresses for gateway and other services
        # Assign an IP address to each service, regardless of whether it is needed or not
        return {app.value: hosts[i + 16] for i, app in enumerate((*ECoreService, *EApp))}

    @property
    def local_ip(self) -> IPv4Address:
        if self._local_ip is None:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                try:
                    s.settimeout(0)
                    s.connect(("10.254.254.254", 1))

                    self._local_ip = IPv4Address(s.getsockname()[0])
                except Exception:
                    self._local_ip = IPv4Address("127.0.0.1")

        return self._local_ip

    @property
    def context(self) -> Context:
        return Context(
            constants=self.constants,
            config=self.config,
            users=self.users,
            plugin_outputs=self.plugin_outputs,
            app_dirs=self.app_dirs,
            dev=self.dev,
            ip_addresses=self.ip_addresses,
            local_ip=self.local_ip,
        )
