import os
from os import PathLike

from typer import Exit

from .console import Console
from .constants import DOCKER_URL, PODMAN_COMPOSE_URL, PODMAN_URL
from ..helpers.common import format_command, format_program, program_exists, run_shell_command
from ..models.container import ContainerService, ContainerTool

docker = format_program("Docker")
podman = format_program("Podman")
podman_compose = format_program("podman-compose")
docker_link = f"[link={DOCKER_URL}]{docker}[/link]"
podman_link = f"[link={PODMAN_URL}]{podman}[/link]"
podman_compose_link = f"[link={PODMAN_COMPOSE_URL}]{podman_compose}[/link]"


class Container:
    """Communicate with the container management tool."""

    def __init__(self, console: Console, working_dir: str | PathLike[str]):
        self.console = console
        self.working_dir = working_dir

    def run_shell_command(self, *command: str):
        """Run a shell command."""
        try:
            env = os.environ.copy()

            if not env.get("XDG_CACHE_HOME"):
                env["XDG_CACHE_HOME"] = os.path.expanduser("~/.cache")
            if not env.get("XDG_CONFIG_HOME"):
                env["XDG_CONFIG_HOME"] = os.path.expanduser("~/.config")
            if not env.get("XDG_DATA_HOME"):
                env["XDG_DATA_HOME"] = os.path.expanduser("~/.local/share")

            run_shell_command(*command, cwd=self.working_dir, env=env)
        except Exception as e:
            self.console.print_error(f"An error occurred while running command {format_command(command)} ({e}).")
            raise Exit(code=1)

    def choose_tool(self) -> ContainerTool:
        if program_exists("docker"):
            self.console.print(f"Found {docker}. Use {docker} for the following operations.")
            return ContainerTool.DOCKER
        elif program_exists("podman"):
            if program_exists("podman-compose"):
                self.console.print(f"Found {podman}. Use {podman} for the following operations.")
                return ContainerTool.PODMAN
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

    def build(self, service: ContainerService | None = None, force_rebuild: bool = False):
        with self.console.status("Building container images..."):
            match self.choose_tool():
                case ContainerTool.DOCKER:
                    self.run_shell_command(
                        "docker",
                        "compose",
                        "build",
                        service.value if service else "",
                        "--no-cache" if force_rebuild else "",
                    )
                case ContainerTool.PODMAN:
                    self.run_shell_command(
                        "podman-compose",
                        "build",
                        service.value if service else "",
                        "--no-cache" if force_rebuild else "",
                    )

    def up(self, ensure_built: bool = False):
        with self.console.status("Starting containers..."):
            match self.choose_tool():
                case ContainerTool.DOCKER:
                    self.run_shell_command("docker", "compose", "up", "-d", "--build" if ensure_built else "")
                case ContainerTool.PODMAN:
                    self.run_shell_command("podman-compose", "up", "-d", "--build" if ensure_built else "")

    def down(self):
        with self.console.status("Stopping containers..."):
            match self.choose_tool():
                case ContainerTool.DOCKER:
                    self.run_shell_command("docker", "compose", "down")
                case ContainerTool.PODMAN:
                    self.run_shell_command("podman-compose", "down")

    def run(self, service: ContainerService, *command: str, ensure_built: bool = False, force_rebuild: bool = False):
        if ensure_built:
            self.build(service, force_rebuild)

        with self.console.status(f"Running command {format_command(command)} in {format_program(service.value)}..."):
            match self.choose_tool():
                case ContainerTool.DOCKER:
                    self.run_shell_command("docker", "compose", "run", service.value, *command)
                case ContainerTool.PODMAN:
                    self.run_shell_command("podman-compose", "run", service.value, *command)
