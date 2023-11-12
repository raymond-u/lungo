import subprocess
from os import PathLike

from typer import Exit

from .console import Console
from .constants import APP_NAME_CAPITALIZED, DOCKER_URL, PODMAN_COMPOSE_URL, PODMAN_URL
from .context import ContextManager
from .file import FileUtils
from .storage import Storage
from ..helpers.common import format_command, format_link, format_program, program_exists
from ..models.base import EContainer, EService

_docker = format_program("Docker")
_podman = format_program("Podman")
_podman_compose = format_program("podman-compose")
_docker_link = format_link(DOCKER_URL, _docker)
_podman_link = format_link(PODMAN_URL, _podman)
_podman_compose_link = format_link(PODMAN_COMPOSE_URL, _podman_compose)


class Container:
    """Communicate with the container management tool."""

    def __init__(self, console: Console, file_utils: FileUtils, storage: Storage, context_manager: ContextManager):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self.context_manager = context_manager
        self.preferred_tool = None
        self.tool = None

    def set_preferred_tool(self, tool: EContainer | None) -> None:
        self.preferred_tool = tool

    def run_shell_command(
        self, *command: str, cwd: str | PathLike[str] | None = None, capture_output: bool = False
    ) -> str | None:
        command = list(filter(None, command))

        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    check=True,
                    cwd=cwd or self.storage.bundled_dir,
                    text=True,
                )
                return result.stdout
            else:
                subprocess.run(
                    command,
                    check=True,
                    cwd=cwd or self.storage.bundled_dir,
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )
                return None
        except Exception as e:
            self.console.print_error(f"Failed to run command {format_command(*command)} ({e}).")
            raise Exit(code=1)

    def choose_tool(self) -> EContainer:
        if self.tool:
            return self.tool

        if self.preferred_tool == EContainer.DOCKER or (self.preferred_tool is None and program_exists("docker")):
            self.console.print_info(f"Found {_docker}. Use {_docker} for the following operations.")
            self.tool = EContainer.DOCKER

            if self.context_manager.config.security.rate_limiting.enabled:
                self.console.print_error(
                    f"The rate limiting feature is not supported on {_docker}. Please use {_podman} instead."
                )
                raise Exit(code=1)

            return EContainer.DOCKER
        elif self.preferred_tool == EContainer.PODMAN or (self.preferred_tool is None and program_exists("podman")):
            if program_exists("podman-compose"):
                self.console.print_info(f"Found {_podman}. Use {_podman} for the following operations.")
                self.tool = EContainer.PODMAN

                return EContainer.PODMAN
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
            case EContainer.DOCKER:
                self.run_shell_command(
                    "docker",
                    "compose",
                    "build",
                    service.value if service else "",
                    "--no-cache" if force_build else "",
                    cwd=working_dir,
                )
            case EContainer.PODMAN:
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

        tool = self.choose_tool()

        if not working_dir:
            self.file_utils.create(self.storage.lock_file)

        match tool:
            case EContainer.DOCKER:
                self.run_shell_command("docker", "compose", "up", "-d", "--build", cwd=working_dir)
            case EContainer.PODMAN:
                if self.context_manager.config.security.rate_limiting.enabled:
                    self.run_shell_command(
                        "podman-compose", "--podman-run-args=--net=pasta", "up", "-d", "--build", cwd=working_dir
                    )
                else:
                    self.run_shell_command("podman-compose", "up", "-d", "--build", cwd=working_dir)

    def down(self, working_dir: str | PathLike[str] | None = None) -> None:
        match self.choose_tool():
            case EContainer.DOCKER:
                self.run_shell_command("docker", "compose", "down", cwd=working_dir)
            case EContainer.PODMAN:
                self.run_shell_command("podman-compose", "down", cwd=working_dir)

        if not working_dir:
            self.file_utils.remove(self.storage.lock_file)
