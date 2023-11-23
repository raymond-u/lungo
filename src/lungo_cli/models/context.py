from ipaddress import IPv4Address
from uuid import UUID

from pydantic import AnyHttpUrl, DirectoryPath, EmailStr

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
    jupyterhub: IPv4Address
    privatebin: IPv4Address
    rstudio: IPv4Address
    xray: IPv4Address


class XrayAccount(Base):
    email: EmailStr
    id: UUID


class Context(Base):
    config: Config
    users: Users
    app_dirs: AppDirs
    base_url: AnyHttpUrl
    ip_addresses: IpAddresses
    dev: bool
    jupyterhub_password: str
    rstudio_password: str
    xray_accounts: list[XrayAccount]
    xray_salt: UUID
