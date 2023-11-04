from datetime import timedelta
from ipaddress import IPv4Network

from pydantic import DirectoryPath, EmailStr, field_validator, FilePath, NewPath

from .base import AllowedApps, Base, EApp, FileName, Port


class Branding(Base):
    name: str = "Lungo"
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


class FileBrowserSettings(Base):
    enabled: bool = True


class JupyterHubSettings(Base):
    enabled: bool = True
    password: str | None = None


class PrivateBin(Base):
    enabled: bool = True


class RStudioSettings(Base):
    enabled: bool = True
    password: str | None = None


class Modules(Base):
    filebrowser: FileBrowserSettings = FileBrowserSettings()
    jupyterhub: JupyterHubSettings = JupyterHubSettings()
    privatebin: PrivateBin = PrivateBin()
    rstudio: RStudioSettings = RStudioSettings()


class Network(Base):
    hostname: str
    subnet: IPv4Network = "192.168.2.0/24"
    http: Http = Http()
    https: Https = Https()


class Privilege(Base):
    allowed_apps: AllowedApps


class Privileges(Base):
    unregistered: Privilege = Privilege(allowed_apps=[])
    guest: Privilege = Privilege(allowed_apps=[EApp.FILEBROWSER, EApp.PRIVATEBIN])
    user: Privilege = Privilege(allowed_apps=[EApp.JUPYTERHUB, EApp.RSTUDIO])
    admin: Privilege = Privilege(allowed_apps="all")


class Rules(Base):
    privileges: Privileges = Privileges()


class Session(Base):
    lifetime: timedelta = timedelta(days=1)


class Security(Base):
    session: Session = Session()


class Smtp(Base):
    host: str
    port: Port
    username: str
    password: str
    name: str = "Lungo"
    sender: EmailStr


class Config(Base):
    branding: Branding = Branding()
    directories: Directories
    modules: Modules = Modules()
    network: Network
    rules: Rules = Rules()
    security: Security = Security()
    smtp: Smtp
