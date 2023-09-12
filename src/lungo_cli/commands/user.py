from typing import Annotated, Optional

from typer import Argument, Option, Typer

from ..app.state import console, users_file
from ..helpers.app import (
    gather_user_info,
    get_user_by_usernames,
    handle_common_args,
    print_user_info,
)
from ..models.user import UserRole

app = Typer(
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)


@app.callback(rich_help_panel="Command Groups")
def main():
    """
    Manage users.
    """
    ...


@app.command()
def add(
    usernames: Annotated[
        Optional[list[str]], Argument(help="The username of the user to add.", show_default=False)
    ] = None,
    full_names: Annotated[
        Optional[list[str]], Option("--full-name", "-n", help="The full name of the user to add.", show_default=False)
    ] = None,
    emails: Annotated[
        Optional[list[str]], Option("--email", "-e", help="The email address of the user to add.", show_default=False)
    ] = None,
    user_roles: Annotated[
        Optional[list[UserRole]], Option("--user-role", "-r", help="The role of the user to add.", show_default=False)
    ] = None,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Add a user.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Gather user information
    users = users_file().load()
    count = gather_user_info(users, usernames, full_names, emails, user_roles)
    users_file().save(users)

    console().print(f"Successfully added {count} account(s).")


@app.command()
def enable(
    usernames: Annotated[
        Optional[list[str]], Argument(help="The username of the user to activate.", show_default=False)
    ] = None,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Activate a user's account.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Activate users
    users = users_file().load()
    users_found = get_user_by_usernames(users, usernames)

    for user in users_found:
        user.user_disabled = False

    users_file().save(users)
    console().print(f"Successfully activated {len(users_found)} account(s).")


@app.command()
def disable(
    usernames: Annotated[
        Optional[list[str]], Argument(help="The username of the user to activate.", show_default=False)
    ] = None,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Suspend a user's account.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Suspend users
    users = users_file().load()
    users_found = get_user_by_usernames(users, usernames)

    for user in users_found:
        user.user_disabled = True

    users_file().save(users)
    console().print(f"Successfully suspended {len(users_found)} account(s).")


@app.command()
def show(
    usernames: Annotated[
        Optional[list[str]], Argument(help="The username of the user to activate.", show_default=False)
    ] = None,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Show information about a user.
    """
    # Handle common arguments
    handle_common_args(quiet)

    # Show information about users
    users = users_file().load()
    users_found = get_user_by_usernames(users, usernames)

    print_user_info(users_found)
