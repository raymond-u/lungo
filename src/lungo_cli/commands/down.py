from typing import Annotated

from typer import Option

from ..app.state import console, container
from ..helpers.app import check_prerequisites, handle_common_args


def main(
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Bring the service offline.
    """
    handle_common_args(quiet)
    check_prerequisites()

    # Stop the service
    container().down()

    console().request_for_newline()
    console().print("Service stopped.")
    console().show_epilogue()
