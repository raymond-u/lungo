import os
import pwd
import re
import tempfile
from os import PathLike
from typing import Iterable

from ruamel.yaml import YAML
from typer import Exit

from .console import Console
from .constants import AUTHELIA_DEFAULT_PASSWORD, AUTHELIA_DEFAULT_PASSWORD_HASH, FILEBROWSER_DEFAULT_PASSWORD_HASH
from .container import Container
from .files import AppFiles
from ..helpers.common import format_input, format_path
from ..models.container import ContainerService
from ..models.user import User, UserRole


class FlatFile:
    """Flat files."""

    def __init__(self, console: Console):
        self.console = console

    def create(self, path: str | PathLike[str]):
        try:
            with open(path, "w"):
                ...
        except Exception as e:
            self.console.print_error(f"Failed to create {format_path(path)} ({e}).")
            raise Exit(code=1)

    def use_temp(self):
        class TempFile:
            def __enter__(self):
                self.temp = tempfile.NamedTemporaryFile("w", delete=False)
                return self.temp

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.temp.close()
                os.unlink(self.temp.name)

        return TempFile()

    def save_env(self, path: str | PathLike[str], **env: str):
        try:
            with open(path, "w") as f:
                for key, value in env.items():
                    f.write(f"{key}='{value}'\n")
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(path)} ({e}).")
            raise Exit(code=1)

    def save_secret(self, path: str | PathLike[str], secret: str):
        try:
            with open(path, "w") as f:
                f.write(secret)
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(path)} ({e}).")
            raise Exit(code=1)


class UsersFile:
    """Files for integral user management."""

    def __init__(self, app_files: AppFiles, console: Console, container: Container):
        self.app_files = app_files
        self.console = console
        self.container = container
        self.password_printed = False
        self.yaml = YAML()

    def load(self) -> list[User]:
        if not self.app_files.authelia_users.is_file():
            return []

        try:
            data = self.yaml.load(self.app_files.authelia_users)
            users = []

            for key, value in data["users"].items():
                if UserRole.ADMIN.value in value["groups"]:
                    user_role = UserRole.ADMIN
                elif UserRole.USER.value in value["groups"]:
                    user_role = UserRole.USER
                else:
                    user_role = UserRole.GUEST

                users.append(
                    User(
                        username=key,
                        full_name=value["displayname"],
                        email=value["email"],
                        user_role=user_role,
                        user_disabled=value["disabled"],
                        password=value["password"],
                    )
                )
        except Exception as e:
            self.console.print_error(f"Failed to read {format_path(self.app_files.authelia_users)} ({e}).")
            raise Exit(code=1)

        return users

    def save(self, users: Iterable[User]):
        # Check the existence of users on the system
        for user in users:
            try:
                pwd.getpwnam(user.username)
            except KeyError:
                self.console.print(
                    (
                        f"User {format_input(user.username)} does not seem to exist on the system. "
                        "You must create it manually."
                    ),
                    epilogue=True,
                )

        self.console.print("Saving user information...")

        # Authelia users
        authelia_data = {"users": {}}

        for user in users:
            if user.user_role == UserRole.ADMIN:
                groups = [UserRole.ADMIN.value, UserRole.USER.value, UserRole.GUEST.value]
            elif user.user_role == UserRole.USER:
                groups = [UserRole.USER.value, UserRole.GUEST.value]
            else:
                groups = [UserRole.GUEST.value]

            authelia_data["users"][user.username] = {
                "disabled": user.user_disabled,
                "displayname": user.full_name,
                "password": user.password,
                "email": user.email,
                "groups": groups,
            }

        try:
            self.yaml.dump(authelia_data, self.app_files.authelia_users)
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(self.app_files.authelia_users)} ({e}).")
            raise Exit(code=1)

        # Filebrowser users
        filebrowser_data = []

        for user in users:
            if user.user_role == UserRole.ADMIN:
                permission = {
                    "admin": True,
                    "execute": True,
                    "create": True,
                    "rename": True,
                    "modify": True,
                    "delete": True,
                    "share": True,
                    "download": True,
                }
            elif user.user_role == UserRole.USER:
                permission = {
                    "admin": False,
                    "execute": False,
                    "create": True,
                    "rename": True,
                    "modify": True,
                    "delete": True,
                    "share": True,
                    "download": True,
                }
            else:
                permission = {
                    "admin": False,
                    "execute": False,
                    "create": False,
                    "rename": False,
                    "modify": False,
                    "delete": False,
                    "share": True,
                    "download": True,
                }

            filebrowser_data.append(
                {
                    "id": 0,
                    "username": user.username,
                    "password": FILEBROWSER_DEFAULT_PASSWORD_HASH,
                    "scope": f"/root/home/{user.username}",
                    "locale": "en",
                    "lockpassword": True,
                    "viewmode": "list",
                    "singleclick": False,
                    "perm": permission,
                    "commands": [],
                    "sorting": {"by": "name", "asc": True},
                    "rules": [],
                    "hidedotfiles": True,
                    "dateformat": False,
                }
            )

        try:
            self.yaml.dump(filebrowser_data, self.app_files.filebrowser_users)
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(self.app_files.filebrowser_users)} ({e}).")
            raise Exit(code=1)

        filebrowser_dockerfile = ["FROM docker.io/filebrowser/filebrowser"]

        for user in users:
            filebrowser_dockerfile.append(f"RUN mkdir -p /root/home/{user.username}")
            filebrowser_dockerfile.append(f"RUN ln -s /mnt/home/{user.username} /root/home/{user.username}/home")
            filebrowser_dockerfile.append(f"RUN ln -s /mnt/home/shared /root/home/{user.username}")
            filebrowser_dockerfile.append(f"RUN ln -s /mnt/home/shared_readonly /root/home/{user.username}")

        try:
            with open(self.app_files.filebrowser_dockerfile, "w") as f:
                f.write("\n".join(filebrowser_dockerfile))
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(self.app_files.filebrowser_dockerfile)} ({e}).")
            raise Exit(code=1)

        if not self.app_files.filebrowser_database.exists():
            self.container.run(
                ContainerService.FILEBROWSER,
                "-c",
                "/etc/filebrowser/settings.yaml",
                "config",
                "init",
                "--auth.method=noauth",
                ensure_built=True,
            )
            self.container.run(
                ContainerService.FILEBROWSER,
                "-c",
                "/etc/filebrowser/settings.yaml",
                "config",
                "import",
                "/etc/filebrowser/config_export.yaml",
                ensure_built=True,
            )

        self.container.run(
            ContainerService.FILEBROWSER,
            "-c",
            "/etc/filebrowser/settings.yaml",
            "users",
            "import",
            "/var/lib/filebrowser/users_export.yaml",
            ensure_built=True,
            force_rebuild=True,
        )

        # RStudio users
        rstudio_dockerfile = ["FROM docker.io/rocker/verse"]

        for user in users:
            rstudio_dockerfile.append(f"RUN useradd -g root -G sudo -m '{user.username}'")
            rstudio_dockerfile.append(f"RUN echo '{user.username}:passwd' | chpasswd")
            rstudio_dockerfile.append(f"RUN ln -s /mnt/home/{user.username} /home/{user.username}/home")
            rstudio_dockerfile.append(f"RUN ln -s /mnt/home/shared /home/{user.username}")
            rstudio_dockerfile.append(f"RUN ln -s /mnt/home/shared_readonly /home/{user.username}")

        try:
            with open(self.app_files.rstudio_dockerfile, "w") as f:
                f.write("\n".join(rstudio_dockerfile))
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(self.app_files.rstudio_dockerfile)} ({e}).")
            raise Exit(code=1)

        self.container.build(ContainerService.RSTUDIO, force_rebuild=True)

    def add(self, users: list[User], user: User) -> bool:
        if not re.fullmatch(r"[\w-]+", user.username):
            self.console.print_warning("Username must only contain alphanumeric characters, underscores, and dashes.")
            return False

        for user_ in users:
            if user_.username == user.username:
                self.console.print_warning("Username must be unique.")
                return False

        if "@" not in user.email:
            self.console.print_warning("Email address must be valid.")
            return False

        if user.password is ...:
            user.password = AUTHELIA_DEFAULT_PASSWORD_HASH

            if not self.password_printed:
                self.console.print(
                    (
                        f"The default password is {format_input(AUTHELIA_DEFAULT_PASSWORD)}. "
                        "Please change it after logging in."
                    ),
                    epilogue=True,
                )
                self.password_printed = True

        users.append(user)
        return True

    def find(self, users: list[User], username: str) -> User | None:
        for user in users:
            if user.username == username:
                return user
        else:
            self.console.print_warning(f"User {format_input(username)} does not exist.")
            return None
