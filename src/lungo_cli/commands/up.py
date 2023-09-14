from pathlib import Path
from typing import Annotated

from typer import Exit, Option

from ..app.state import console, container, users_file
from ..core.constants import APP_NAME
from ..helpers.app import check_prerequisites, handle_common_args
from ..helpers.common import format_command, format_input, format_path


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

    # Check if the shared directories and user home directories exist
    shared_dir = Path.home().parent.joinpath("shared")
    shared_readonly_dir = Path.home().parent.joinpath("shared_readonly")

    if not shared_dir.exists() or not shared_readonly_dir.exists():
        console().print_error(
            f"The {format_path('shared')} and {format_path('shared_readonly')} directories are missing."
            "Please create them and configure their permissions as described in the documentation."
        )
        raise Exit(code=1)

    users = users_file().load()

    for user in users:
        user_home_dir = Path.home().parent.joinpath(user.username)

        if not user_home_dir.exists():
            console().print_error(
                f"The home directory for user {format_input(user.username)} is missing."
                "Please create the user and configure its permissions as described in the documentation."
            )
            raise Exit(code=1)

    # Start the service
    container().up()

    console().request_for_newline()
    console().print("Service is now online.")
    console().print(f"To stop the service, run {format_command(f'{APP_NAME} down')}.")
    console().show_epilogue()
