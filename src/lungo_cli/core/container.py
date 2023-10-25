import subprocess
from enum import auto, Enum
from os import PathLike

from typer import Exit

from .console import Console
from .constants import APP_NAME_CAPITALIZED, DOCKER_URL, PODMAN_COMPOSE_URL, PODMAN_URL
from .file import FileUtils
from .storage import Storage
from ..helpers.common import format_command, format_link, format_program, program_exists
from ..models.base import EService

_docker = format_program("Docker")
_podman = format_program("Podman")
_podman_compose = format_program("podman-compose")
_docker_link = format_link(DOCKER_URL, _docker)
_podman_link = format_link(PODMAN_URL, _podman)
_podman_compose_link = format_link(PODMAN_COMPOSE_URL, _podman_compose)


class EContainerTool(Enum):
    DOCKER = auto()
    PODMAN = auto()


class Container:
    """Communicate with the container management tool."""

    def __init__(self, console: Console, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self.tool = None

    def run_shell_command(
        self, *command: str, cwd: str | PathLike[str] | None = None, show_output: bool = False
    ) -> None:
        command = list(filter(None, command))

        try:
            if show_output:
                subprocess.run(command, check=True, cwd=cwd or self.storage.bundled_dir)
            else:
                subprocess.run(
                    command,
                    check=True,
                    cwd=cwd or self.storage.bundled_dir,
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )
        except Exception as e:
            self.console.print_error(f"Failed to run command {format_command(*command)} ({e}).")
            raise Exit(code=1)

    def choose_tool(self) -> EContainerTool:
        if self.tool:
            return self.tool

        if program_exists("docker"):
            self.console.print_info(f"Found {_docker}. Use {_docker} for the following operations.")
            self.tool = EContainerTool.DOCKER

            return EContainerTool.DOCKER
        elif program_exists("podman"):
            if program_exists("podman-compose"):
                self.console.print_info(f"Found {_podman}. Use {_podman} for the following operations.")
                self.tool = EContainerTool.PODMAN

                return EContainerTool.PODMAN
            else:
                self.console.print_error(
                    f"{_podman_link} is installed, but {_podman_compose_link} is not. "
                    f"Please install {_podman_compose_link}."
                )
                raise Exit(code=1)
        else:
            self.console.print_error(
                (
                    f"Neither {_docker_link} nor {_podman_link} is installed."
                    f"Please install one of them. For {_podman_link}, you will also need {_podman_compose_link}."
                )
            )
            raise Exit(code=1)

    def build(
        self,
        working_dir: str | PathLike[str] | None = None,
        service: EService | None = None,
        force_build: bool = False,
    ) -> None:
        match self.choose_tool():
            case EContainerTool.DOCKER:
                self.run_shell_command(
                    "docker",
                    "compose",
                    "build",
                    service.value if service else "",
                    "--no-cache" if force_build else "",
                    cwd=working_dir,
                )
            case EContainerTool.PODMAN:
                self.run_shell_command(
                    "podman-compose",
                    "build",
                    service.value if service else "",
                    "--no-cache" if force_build else "",
                    cwd=working_dir,
                )

    def up(self, working_dir: str | PathLike[str] | None = None) -> None:
        if self.storage.lock_file.is_file():
            self.console.print_error(
                f"An existing instance of {APP_NAME_CAPITALIZED} is running. Please stop it before proceeding. "
                f"Or, you can remove the restriction forcibly by using the {format_command('--remove-lock')} option."
            )
            raise Exit(code=1)

        if not working_dir:
            self.file_utils.create(self.storage.lock_file)

        match self.choose_tool():
            case EContainerTool.DOCKER:
                self.run_shell_command("docker", "compose", "up", "-d", "--build", cwd=working_dir)
            case EContainerTool.PODMAN:
                self.run_shell_command("podman-compose", "up", "-d", "--build", cwd=working_dir)

    def down(self, working_dir: str | PathLike[str] | None = None) -> None:
        match self.choose_tool():
            case EContainerTool.DOCKER:
                self.run_shell_command("docker", "compose", "down", cwd=working_dir)
            case EContainerTool.PODMAN:
                self.run_shell_command("podman-compose", "down", cwd=working_dir)

        if not working_dir:
            self.file_utils.remove(self.storage.lock_file)
