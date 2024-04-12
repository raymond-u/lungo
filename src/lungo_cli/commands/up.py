from typing import Annotated, Optional

from typer import Exit, Option

from .base import ConfigDirType, DevType, ForceInitType, QuietType, VerbosityType
from ..app.state import app_manager, console, container, context_manager, file_utils, storage
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.common import port_is_available
from ..helpers.format import format_command, format_input, format_link
from ..models.base import EContainer


def main(
    build_only: Annotated[bool, Option("--build-only", help="Only build the containers.", show_default=False)] = False,
    container_tool: Annotated[
        Optional[EContainer], Option("--container-tool", help="Container management tool to use.", show_default=False)
    ] = None,
    render_only: Annotated[
        bool, Option("--render-only", help="Only render the templates.", show_default=False)
    ] = False,
    force_init: ForceInitType = False,
    remove_lock: Annotated[bool, Option("--remove-lock", help="Remove the lock file.", show_default=False)] = False,
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
):
    """
    Start the service.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity, force_init)
    app_manager().load_full_config()

    if remove_lock:
        file_utils().remove(storage().lock_file)

    app_manager().update_app_data()

    if render_only:
        return

    container().set_preferred_tool(container_tool)

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
            f"To stop it, run {format_command(APP_NAME, 'down', '--dev' if context_manager().dev else '')}."
        )
