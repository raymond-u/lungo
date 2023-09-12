from typing import Collection

from typer import Exit

from .common import format_input
from ..app.state import console, users_file
from ..models.user import User, UserRole


def handle_common_args(quiet: bool):
    if quiet:
        console().set_log_level(-1)


def gather_user_info(
    users: list[User],
    usernames: list[str] | None = None,
    full_names: list[str] = None,
    emails: list[str] = None,
    user_roles: list[UserRole] = None,
) -> int:
    # Check the number of elements in each argument
    max_length = 0
    users_initial_length = len(users)

    for arg in (usernames, full_names, emails, user_roles):
        if arg:
            if len(arg) != max_length:
                if max_length == 0:
                    max_length = len(arg)
                else:
                    console().print_error("Non-empty arguments must have the same number of elements.")
                    raise Exit(code=1)

    # If no arguments are provided, ask for user information indefinitely
    if max_length == 0:
        while True:
            count = 1

            while True:
                console().print(f"Please enter information for user {count}. Leave blank to finish.")

                if not (username := console().ask_for_string("Username", guard=lambda x: True)):
                    break
                if not (full_name := console().ask_for_string("Full name", guard=lambda x: True)):
                    break
                if not (email := console().ask_for_string("Email", guard=lambda x: True)):
                    break
                user_role = console().ask_for_enum("User role", UserRole, default=UserRole.USER)

                console().request_for_newline()
                user = User(username=username, full_name=full_name, email=email, user_role=user_role)

                if users_file().add(users, user):
                    count += 1

            console().request_for_newline()

            if not users:
                console().print_warning("You must provide at least one user.")
                continue

            print_user_info(users[users_initial_length:])

            if console().ask_for_boolean("Is this information correct?"):
                break
    else:
        for i in range(max_length):
            prologue_printed = False

            if usernames:
                username = usernames[i]
            else:
                console().print(f"Please enter information for user {i + 1}.")
                prologue_printed = True

                username = console().ask_for_string("Username")

            if full_names:
                full_name = full_names[i]
            else:
                if not prologue_printed:
                    console().print(f"Please enter information for user {format_input(username)}.")
                    prologue_printed = True

                full_name = console().ask_for_string("Full name")

            if emails:
                email = emails[i]
            else:
                if not prologue_printed:
                    console().print(f"Please enter information for user {format_input(username)}.")
                    prologue_printed = True

                email = console().ask_for_string("Email")

            if user_roles:
                user_role = user_roles[i]
            else:
                if not prologue_printed:
                    console().print(f"Please enter information for user {format_input(username)}.")

                user_role = console().ask_for_enum("User role", UserRole, default=UserRole.USER)

            console().request_for_newline()
            user = User(username=username, full_name=full_name, email=email, user_role=user_role)

            users_file().add(users, user)

        print_user_info(users[users_initial_length:])

    return len(users) - users_initial_length


def get_user_by_usernames(users: list[User], usernames: list[str] | None = None) -> list[User]:
    users_found = []

    if not usernames:
        console().print(f"Please enter usernames. Leave blank to finish.")

        while True:
            while True:
                if not (username := console().ask_for_string("Username", guard=lambda x: True)):
                    break

                if user := users_file().find(users, username):
                    users_found.append(user)

            if not users_found:
                console().print_warning("You must provide at least one username.")
                continue

            break
    else:
        for username in usernames:
            if user := users_file().find(users, username):
                users_found.append(user)

    console().request_for_newline()
    return users_found


def print_user_info(users: Collection[User]):
    for index, user in enumerate(users, start=1):
        console().print(f"User {index}/{len(users)}")
        console().print(f"Username:  {format_input(user.username)}")
        console().print(f"Full name: {format_input(user.full_name)}")
        console().print(f"Email:     {format_input(user.email)}")
        console().print(f"User role: {format_input(user.user_role.value)}")

    console().request_for_newline()
