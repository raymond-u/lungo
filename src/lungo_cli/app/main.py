from typing import Annotated

from typer import Exit, Option, Typer

from .state import console
from ..commands import check, down, install, list, uninstall, up
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.common import get_app_version

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)

app.command("check")(check.main)
app.command("up")(up.main)
app.command("down")(down.main)
app.command("list")(list.main)
app.command("install")(install.main)
app.command("uninstall")(uninstall.main)


def app_wrapper():
    app()


def version_callback(value: bool):
    if value:
        version = get_app_version()
        console().print(f"{APP_NAME_CAPITALIZED} {version}")
        raise Exit()


@app.callback(APP_NAME)
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
    A CLI tool for Lungo: a user-friendly home lab setup designed for small-to-mid-scale on-premises hosting.
    """
    ...
