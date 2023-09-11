from typing import Annotated

from typer import Exit, Option, Typer

from .state import console
from ..commands import down, init, up, user
from ..core.constants import APP_NAME_CAPITALIZED
from ..helpers.common import get_app_version

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)

app.command("init")(init.main)
app.command("up")(up.main)
app.command("down")(down.main)

app.add_typer(user.app, name="user")


def app_wrapper():
    app()
    console().show_epilogue()


def version_callback(value: bool):
    if value:
        version = get_app_version()
        console().print(f"{APP_NAME_CAPITALIZED} {version}")
        raise Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        Option(
            "--version",
            "-v",
            callback=version_callback,
            help="Show the version of the program and exit.",
            is_eager=True,
        ),
    ] = False
):
    """
    A CLI tool for managing Lungo, a self-hosted web application suite.
    """
    ...
