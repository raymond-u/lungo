from typing import Annotated

from typer import Option

from ..app.state import console, container
from ..helpers.app import check_prerequisites, handle_common_args


def main(
    attach: Annotated[
        bool, Option("--attach", "-a", help="Attach to the container's output.", show_default=False)
    ] = False,
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
    container().up(not attach)
    console().print("Service is now online.")
