from ipaddress import IPv4Address

from pydantic import ConfigDict, DirectoryPath

from .base import Base
from .config import Config
from .users import Users


class AppDirs(Base):
    cache_dir: DirectoryPath
    generated_dir: DirectoryPath
    managed_dir: DirectoryPath


class IpAddresses(Base):
    nginx: IPv4Address
    keto: IPv4Address
    kratos: IPv4Address
    oathkeeper: IPv4Address
    node: IPv4Address
    filebrowser: IPv4Address
    rstudio: IPv4Address


class Context(Base):
    model_config = ConfigDict(frozen=False)

    config: Config
    users: Users
    app_dirs: AppDirs
    ip_addresses: IpAddresses
    rstudio_password: str
