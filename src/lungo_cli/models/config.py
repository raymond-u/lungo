from datetime import timedelta
from ipaddress import IPv4Address, IPv4Network

from pydantic import ConfigDict, DirectoryPath, EmailStr, field_validator, FilePath, NewPath, PositiveInt

from .base import AllowedApps, Base, FileName, Port
from ..core.constants import APP_NAME_CAPITALIZED


class Branding(Base):
    name: str = APP_NAME_CAPITALIZED
    subtitle: list[str] = ["a hug in a mug", "a poetry of aroma", "a quiet solitude", "a whisper of inspiration"]
    cover: FilePath | None = None
    logo: FilePath | None = None


class SharedDir(Base):
    name: FileName
    source: DirectoryPath | FilePath
    read_only: bool = False

    # noinspection PyNestedDecorators
    @field_validator("name")
    @classmethod
    def name_field_validator(cls, v: str) -> str:
        # Name must not be "home" because it is used as a mount point for the user's home directory
        if v == "home":
            raise ValueError("must not be 'home'")

        return v


class Directories(Base):
    cache_dir: DirectoryPath | NewPath | None = None
    data_dir: DirectoryPath | NewPath | None = None
    users_dir: DirectoryPath | NewPath
    shared_dirs: list[SharedDir] = []


class Http(Base):
    enabled: bool = True
    port: Port = 80


class Tls(Base):
    cert: FilePath
    key: FilePath


class Https(Base):
    port: Port = 443
    tls: Tls | None = None


class Network(Base):
    hostname: str
    subnet: IPv4Network = IPv4Network("192.168.2.0/24")
    trusted_proxies: list[IPv4Address] = []
    http: Http = Http()
    https: Https = Https()


class Plugins(Base):
    model_config = ConfigDict(extra="ignore")


class Privilege(Base):
    allowed_apps: AllowedApps


class Privileges(Base):
    unregistered: Privilege = Privilege(allowed_apps=[])
    guest: Privilege = Privilege(allowed_apps=[])
    user: Privilege = Privilege(allowed_apps=[])
    admin: Privilege = Privilege(allowed_apps="all")


class Rules(Base):
    privileges: Privileges = Privileges()


class RateLimiting(Base):
    enabled: bool = False
    max_requests: PositiveInt = 5
    time_window: timedelta = timedelta(hours=1)


class Session(Base):
    lifetime: timedelta = timedelta(days=1)


class Security(Base):
    rate_limiting: RateLimiting = RateLimiting()
    session: Session = Session()


class Smtp(Base):
    host: str
    port: Port
    username: str
    password: str
    name: str = APP_NAME_CAPITALIZED
    sender: EmailStr


class Config(Base):
    branding: Branding = Branding()
    directories: Directories
    network: Network
    plugins: Plugins = Plugins()
    rules: Rules = Rules()
    security: Security = Security()
    smtp: Smtp
