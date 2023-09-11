from typing import Annotated

from typer import Option

from ..app.state import container
from ..helpers.app import handle_common_args


def main(
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
    Bring the service offline.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Stop the service
    container().down()
