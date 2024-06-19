import subprocess
from os import PathLike

from typer import Exit

from .console import Console, LogLevels
from .constants import APP_NAME_CAPITALIZED, DOCKER_COMPOSE_URL, DOCKER_URL, PODMAN_COMPOSE_URL, PODMAN_URL
from .context import ContextManager
from .file import FileUtils
from .storage import Storage
from ..helpers.common import program_exists
from ..helpers.format import format_command, format_link, format_program
from ..models.base import EApp, EContainer, ECoreService

_docker = format_program("Docker")
_docker_link = format_link(DOCKER_URL, _docker)
_docker_compose = format_program("Docker Compose")
_docker_compose_link = format_link(DOCKER_COMPOSE_URL, _docker_compose)
_podman = format_program("Podman")
_podman_link = format_link(PODMAN_URL, _podman)
_podman_compose = format_program("Podman Compose")
_podman_compose_link = format_link(PODMAN_COMPOSE_URL, _podman_compose)


class Container:
    """Communicate with the container management tool."""

    def __init__(self, console: Console, context_manager: ContextManager, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.storage = storage

        self.preferred_tool = None
        self.tool = None

    def set_preferred_tool(self, tool: EContainer | None) -> None:
        self.preferred_tool = tool

    def run_shell_command(self, *command: str, cwd: str | PathLike[str] | None = None) -> None:
        command = list(filter(None, command))

        try:
            if self.console.log_level < LogLevels.INFO:
                with subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=cwd or self.storage.bundled_dir,
                ) as process:
                    self.console.print_debug(f"Streaming the output of command {format_command(*command)}.")
                    self.console.request_newline()

                    for line in process.stdout:
                        self.console.print(line.decode(), end="")

                    self.console.request_newline()

                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, command)
            else:
                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=cwd or self.storage.bundled_dir,
                    check=True,
                )
        except Exception as e:
            self.console.print_error(f"Failed to run command {format_command(*command)} ({e}).")
            raise Exit(code=1)

    def choose_tool(self) -> EContainer:
        if self.tool:
            return self.tool

        match self.preferred_tool:
            case EContainer.DOCKER:
                if program_exists("docker"):
                    self.tool = EContainer.DOCKER
                    return EContainer.DOCKER
                else:
                    self.console.print_error(f"{_docker_link} is not installed.")
                    raise Exit(code=1)
            case EContainer.DOCKER_COMPOSE:
                if program_exists("podman"):
                    if program_exists("docker-compose"):
                        self.tool = EContainer.DOCKER_COMPOSE
                        return EContainer.DOCKER_COMPOSE
                    else:
                        self.console.print_error(f"{_docker_compose_link} is not installed.")
                        raise Exit(code=1)
                else:
                    self.console.print_error(f"{_podman_link} is not installed.")
                    raise Exit(code=1)
            case EContainer.PODMAN_COMPOSE:
                if program_exists("podman"):
                    if program_exists("podman-compose"):
                        self.tool = EContainer.PODMAN_COMPOSE
                        return EContainer.PODMAN_COMPOSE
                    else:
                        self.console.print_error(f"{_podman_compose_link} is not installed.")
                        raise Exit(code=1)
                else:
                    self.console.print_error(f"{_podman_link} is not installed.")
                    raise Exit(code=1)

        if program_exists("docker"):
            self.console.print_info(f"Found {_docker}. Use {_docker} for the following operations.")
            self.tool = EContainer.DOCKER

            return EContainer.DOCKER
        elif program_exists("podman"):
            if program_exists("podman-compose"):
                self.console.print_info(f"Found {_podman_compose}. Use {_podman_compose} for the following operations.")
                self.tool = EContainer.PODMAN_COMPOSE

                return EContainer.PODMAN_COMPOSE
            elif program_exists("docker-compose"):
                self.console.print_info(f"Found {_docker_compose}. Use {_docker_compose} for the following operations.")
                self.tool = EContainer.DOCKER_COMPOSE

                return EContainer.DOCKER_COMPOSE
            else:
                self.console.print_error(f"Neither {_docker_compose_link} nor {_podman_compose_link} is installed.")
                raise Exit(code=1)
        else:
            self.console.print_error(f"Neither {_docker_link} nor {_podman_link} is installed.")
            raise Exit(code=1)

    def build(self, working_dir: str | PathLike[str] | None = None, service: EApp | ECoreService | None = None) -> None:
        match self.choose_tool():
            case EContainer.DOCKER:
                self.run_shell_command("docker", "compose", "build", service.value if service else "", cwd=working_dir)
            case EContainer.DOCKER_COMPOSE:
                self.run_shell_command("docker-compose", "build", service.value if service else "", cwd=working_dir)
            case EContainer.PODMAN_COMPOSE:
                self.run_shell_command("podman-compose", "build", service.value if service else "", cwd=working_dir)

    def up(self, working_dir: str | PathLike[str] | None = None) -> None:
        if self.storage.lock_file.is_file():
            self.console.print_error(
                f"An existing instance of {APP_NAME_CAPITALIZED} is running. Please stop it before proceeding, "
                f"or use the {format_command('--remove-lock')} flag."
            )
            raise Exit(code=1)

        tool = self.choose_tool()

        if not working_dir:
            self.file_utils.create(self.storage.lock_file)

        try:
            match tool:
                case EContainer.DOCKER:
                    self.run_shell_command("docker", "compose", "up", "-d", "--build", cwd=working_dir)
                case EContainer.DOCKER_COMPOSE:
                    self.run_shell_command("docker-compose", "up", "-d", "--build", cwd=working_dir)
                case EContainer.PODMAN_COMPOSE:
                    self.run_shell_command("podman-compose", "up", "-d", "--build", cwd=working_dir)
        except Exception:
            self.file_utils.remove(self.storage.lock_file)
            raise

    def down(self, working_dir: str | PathLike[str] | None = None) -> None:
        match self.choose_tool():
            case EContainer.DOCKER:
                self.run_shell_command("docker", "compose", "down", cwd=working_dir)
            case EContainer.DOCKER_COMPOSE:
                self.run_shell_command("docker-compose", "down", cwd=working_dir)
            case EContainer.PODMAN_COMPOSE:
                self.run_shell_command("podman-compose", "down", cwd=working_dir)

        if not working_dir:
            self.file_utils.remove(self.storage.lock_file)
