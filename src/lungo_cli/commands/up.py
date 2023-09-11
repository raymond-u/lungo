from typing import Annotated

from typer import Exit, Option

from ..app.state import app_files, console, container
from ..core.constants import APP_NAME
from ..helpers.app import handle_common_args
from ..helpers.common import format_command


def main(
    attach: Annotated[
        bool,
        Option(
            "--attach",
            "-a",
            help="Attach to the container's output.",
            show_default=False,
        ),
    ] = False,
    quiet: Annotated[
        bool,
        Option(
            "--quiet",
            "-q",
            help="Suppress all output except for errors.",
            show_default=False,
        ),
    ] = False,
):
    """
    Bring the service online.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Check if config files exist
    if not app_files().config_dir.exists():
        console().print_error(f"No configuration files found. Please run {format_command(f'{APP_NAME} init')} first.")
        raise Exit(code=1)

    # Start the service
    container().up(not attach)
