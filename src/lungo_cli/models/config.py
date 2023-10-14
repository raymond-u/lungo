from ipaddress import IPv4Network

from pydantic import DirectoryPath, EmailStr, FilePath, NewPath

from .base import AllowedApps, Base, EApp, Port


class Branding(Base):
    name: str = "Lungo"
    cover: FilePath | None = None
    logo: FilePath | None = None


class SharedDir(Base):
    name: str
    source: DirectoryPath | FilePath
    read_only: bool = False


class Directories(Base):
    cache_dir: DirectoryPath | NewPath | None = None
    data_dir: DirectoryPath | NewPath | None = None
    user_dir: DirectoryPath | NewPath | None = None
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
    subnet: IPv4Network = "192.168.2.0/24"
    http: Http = Http()
    https: Https = Https()


class Privilege(Base):
    allowed_apps: AllowedApps


class Privileges(Base):
    unregistered: Privilege = Privilege(allowed_apps=[])
    guest: Privilege = Privilege(allowed_apps=[EApp.FILEBROWSER])
    user: Privilege = Privilege(allowed_apps=[EApp.RSTUDIO])
    admin: Privilege = Privilege(allowed_apps="all")


class Rules(Base):
    privileges: Privileges = Privileges()


class Smtp(Base):
    host: str
    port: Port
    username: str
    password: str
    name: str = "Lungo"
    sender: EmailStr


class Config(Base):
    branding: Branding = Branding()
    directories: Directories = Directories()
    network: Network
    rules: Rules = Rules()
    smtp: Smtp
