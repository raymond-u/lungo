from uuid import UUID, uuid5

from typer import Exit

from .console import Console
from .file import FileUtils
from .storage import Storage
from ..helpers.format import format_input
from ..models.config import Config
from ..models.context import AppDirs, Context, IpAddresses, XrayAccount
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
    def base_url(self) -> str:
        port = f":{self.config.network.https.port}" if self.config.network.https.port != 443 else ""
        return f"https://{self.config.network.hostname}{port}/"

    @property
    def ip_addresses(self) -> IpAddresses:
        if self.config.network.subnet.num_addresses < 256:
            self.console.print_error(
                f"Subnet {format_input(str(self.config.network.subnet))} is too small. "
                "Please change it to a subnet with at least 256 addresses."
            )
            raise Exit(code=1)

        hosts = list(self.config.network.subnet.hosts())

        return IpAddresses(
            nginx=hosts[100],
            keto=hosts[101],
            kratos=hosts[102],
            oathkeeper=hosts[103],
            node=hosts[104],
            filebrowser=hosts[105],
            jupyterhub=hosts[106],
            privatebin=hosts[107],
            rstudio=hosts[108],
            xray=hosts[109],
        )

    @property
    def dev(self) -> bool:
        return self._dev

    @dev.setter
    def dev(self, value: bool):
        self._dev = value

    @property
    def jupyterhub_password(self) -> str:
        return self.config.modules.jupyterhub.password or self.file_utils.read_text(
            self.storage.jupyterhub_password_file
        )

    @property
    def rstudio_password(self) -> str:
        return self.config.modules.rstudio.password or self.file_utils.read_text(self.storage.rstudio_password_file)

    @property
    def xray_accounts(self) -> list[XrayAccount]:
        return [
            XrayAccount(email=account.email, id=uuid5(self.xray_salt, account.username))
            for account in self.users.accounts
        ]

    @property
    def xray_salt(self) -> UUID:
        return UUID(self.file_utils.read_text(self.storage.xray_salt_file))

    @property
    def context(self) -> Context:
        return Context(
            config=self.config,
            users=self.users,
            app_dirs=self.app_dirs,
            base_url=self.base_url,
            ip_addresses=self.ip_addresses,
            dev=self.dev,
            jupyterhub_password=self.jupyterhub_password,
            rstudio_password=self.rstudio_password,
            xray_accounts=self.xray_accounts,
            xray_salt=self.xray_salt,
        )
