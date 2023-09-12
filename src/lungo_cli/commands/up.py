from typing import Annotated

from typer import Option

from ..app.state import console, container
from ..core.constants import APP_NAME
from ..helpers.app import check_prerequisites, handle_common_args
from ..helpers.common import format_command


def main(
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Bring the service online.
    """
    handle_common_args(quiet)
    check_prerequisites()

    # Start the service
    container().up()
    console().print("Service is now online.")
    console().print(f"To stop the service, run {format_command(f'{APP_NAME} down')}.")
