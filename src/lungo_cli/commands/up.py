from typing import Annotated, Optional

from typer import Exit, Option

from .base import config_dir_type, dev_type, force_init_type, quiet_type, verbosity_type
from ..app.state import app_manager, console, container, context_manager, file_utils, storage
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.common import port_is_available
from ..helpers.format import format_command, format_input, format_link
from ..models.base import EContainer


def main(
    build_only: Annotated[bool, Option("--build-only", help="Only build the container.", show_default=False)] = False,
    container_tool: Annotated[
        Optional[EContainer], Option("--container-tool", help="Container management tool to use.", show_default=False)
    ] = None,
    force_init: force_init_type = False,
    remove_lock: Annotated[bool, Option("--remove-lock", help="Remove the lock file.", show_default=False)] = False,
    config_dir: config_dir_type = None,
    dev: dev_type = False,
    quiet: quiet_type = False,
    verbosity: verbosity_type = 0,
):
    """
    Start the service.
    """
    app_manager().process_args(config_dir, dev, quiet, verbosity, force_init)
    app_manager().load_config_and_plugins()
    app_manager().update_app_data()

    container().set_preferred_tool(container_tool)

    if remove_lock:
        file_utils().remove(storage().lock_file)

    if build_only:
        with console().status(
            "Building containers (could take a few minutes, depending on the internet connection)..."
        ):
            container().build()

        console().print("Build completed.")
    else:
        http_port = context_manager().config.network.http.port
        https_port = context_manager().config.network.https.port

        if context_manager().config.network.http.enabled and not port_is_available(http_port):
            console().print_error(f"Port {format_input(http_port)} is in use.")
            raise Exit(code=1)

        if not port_is_available(https_port):
            console().print_error(f"Port {format_input(https_port)} is in use.")
            raise Exit(code=1)

        with console().status(
            "Starting the service (could take a few minutes, depending on the internet connection)..."
        ):
            container().up()

        console().print(
            f"{APP_NAME_CAPITALIZED} is now available at {format_link(context_manager().base_url)}. "
            f"To stop it, run {format_command(APP_NAME, 'down')}."
        )
