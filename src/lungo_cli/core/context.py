from ipaddress import IPv4Network

from typer import Exit

from .console import Console
from .file import FileUtils
from .storage import Storage
from ..helpers.common import format_input
from ..models.config import Config
from ..models.context import AppDirs, Context, IpAddresses
from ..models.users import Users


class ContextManager:
    """Manage the context of the application, can be passed to the renderer to render templates."""

    def __init__(self, console: Console, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self._config = None
        self._users = None
        self._dev = False

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
    def app_dirs(self) -> AppDirs:
        return AppDirs(
            cache_dir=self.storage.cache_latest_dir,
            generated_dir=self.storage.generated_dir,
            managed_dir=self.storage.managed_dir,
        )

    @property
    def ip_addresses(self) -> IpAddresses:
        subnet = IPv4Network(self.config.network.subnet)

        if subnet.num_addresses < 256:
            self.console.print_error(
                f"Subnet {format_input(str(subnet))} is too small. "
                "Please change it to a subnet with at least 256 addresses."
            )
            raise Exit(code=1)

        hosts = list(subnet.hosts())

        return IpAddresses(
            nginx=hosts[100],
            keto=hosts[101],
            kratos=hosts[102],
            oathkeeper=hosts[103],
            node=hosts[104],
            filebrowser=hosts[105],
            rstudio=hosts[106],
        )

    @property
    def dev(self) -> bool:
        return self._dev

    @dev.setter
    def dev(self, value: bool):
        self._dev = value

    @property
    def rstudio_password(self) -> str:
        return self.file_utils.read_text(self.storage.rstudio_password_file)

    @property
    def context(self) -> Context:
        return Context(
            config=self.config,
            users=self.users,
            app_dirs=self.app_dirs,
            ip_addresses=self.ip_addresses,
            debug=self.dev,
            rstudio_password=self.rstudio_password,
        )
