from os import PathLike

from typer import Exit

from .console import Console
from .constants import DOCKER_URL, PODMAN_COMPOSE_URL, PODMAN_URL
from .storage import Storage
from ..helpers.app import run_shell_command
from ..helpers.common import format_command, format_program, program_exists
from ..helpers.file import create, remove
from ..models.container import EContainerService, EContainerTool

docker = format_program("Docker")
podman = format_program("Podman")
podman_compose = format_program("podman-compose")
docker_link = f"[link={DOCKER_URL}]{docker}[/link]"
podman_link = f"[link={PODMAN_URL}]{podman}[/link]"
podman_compose_link = f"[link={PODMAN_COMPOSE_URL}]{podman_compose}[/link]"


class Container:
    """Communicate with the container management tool."""

    def __init__(self, console: Console, storage: Storage):
        self.console = console
        self.storage = storage
        self.tool = None

    def choose_tool(self) -> EContainerTool:
        if self.tool:
            return self.tool

        if program_exists("docker"):
            self.console.print_info(f"Found {docker}. Use {docker} for the following operations.")
            self.tool = EContainerTool.DOCKER

            return EContainerTool.DOCKER
        elif program_exists("podman"):
            if program_exists("podman-compose"):
                self.console.print_info(f"Found {podman}. Use {podman} for the following operations.")
                self.tool = EContainerTool.PODMAN

                return EContainerTool.PODMAN
            else:
                self.console.print_error(
                    f"{podman} is installed, but {podman_compose_link} is not. Please install {podman_compose_link}."
                )
                raise Exit(code=1)
        else:
            self.console.print_error(
                (
                    f"Neither {docker_link} nor {podman_link} is installed."
                    f"Please install one of them. For {podman_link}, you will also need {podman_compose_link}."
                )
            )
            raise Exit(code=1)

    def build(
        self,
        working_dir: str | PathLike[str] | None = None,
        service: EContainerService | None = None,
        force_build: bool = False,
    ) -> None:
        match self.choose_tool():
            case EContainerTool.DOCKER:
                run_shell_command(
                    "docker",
                    "compose",
                    "build",
                    service.value if service else "",
                    "--no-cache" if force_build else "",
                    cwd=working_dir or self.storage.bundled_dir,
                )
            case EContainerTool.PODMAN:
                run_shell_command(
                    "podman-compose",
                    "build",
                    service.value if service else "",
                    "--no-cache" if force_build else "",
                    cwd=working_dir or self.storage.bundled_dir,
                )

    def up(self, working_dir: str | PathLike[str] | None = None) -> None:
        if self.storage.lock_file.is_file():
            self.console.print_error(
                "Another instance of Lungo is already running. Please stop it first. "
                f"Or, you can forcefully remove the lock by using the {format_command('--remove-lock')} option."
            )
            raise Exit(code=1)

        if not working_dir:
            create(self.storage.lock_file)

        match self.choose_tool():
            case EContainerTool.DOCKER:
                run_shell_command(
                    "docker", "compose", "up", "-d", "--build", cwd=working_dir or self.storage.bundled_dir
                )
            case EContainerTool.PODMAN:
                run_shell_command("podman-compose", "up", "-d", "--build", cwd=working_dir or self.storage.bundled_dir)

    def down(self, working_dir: str | PathLike[str] | None = None) -> None:
        match self.choose_tool():
            case EContainerTool.DOCKER:
                run_shell_command("docker", "compose", "down", cwd=working_dir or self.storage.bundled_dir)
            case EContainerTool.PODMAN:
                run_shell_command("podman-compose", "down", cwd=working_dir or self.storage.bundled_dir)

        if not working_dir:
            remove(self.storage.lock_file)
