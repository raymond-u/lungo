from typing import Annotated, Optional

from typer import Exit, Option

from ..app.state import app_files, console, flat_file, users_file
from ..helpers.app import gather_user_info, handle_common_args, reset_app
from ..helpers.crypto import generate_random_string, generate_self_signed_cert
from ..models.user import UserRole


def main(
    usernames: Annotated[
        Optional[list[str]], Option("--username", "-u", help="The username of the user to add.", show_default=False)
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
    force: Annotated[
        bool, Option("--force", "-f", help="Force initialization even if already initialized.", show_default=False)
    ] = False,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
):
    """
    Initialize config files and containers. Must be run before first use.
    """
    try:
        handle_common_args(quiet)

        # Remove existing configuration files if force is enabled
        if force:
            console().print("Removing existing configuration files...")
            reset_app()

        # Ensure that directories exist
        for dir_ in app_files().all_directories:
            dir_.mkdir(parents=True, exist_ok=True)

        # Generate env and secret files for Authelia
        if not app_files().authelia_env.exists():
            domain_name = console().ask_for_string("Please enter the domain name of your website")
            brand_name = console().ask_for_string("Please enter the brand name of your website")
            email_address = console().ask_for_string(
                "Please enter the email address for notification service",
                guard=lambda x: "@" in x,
            )
            smtp_host = console().ask_for_string(
                "Please enter the SMTP server address associated with the email address"
            )
            smtp_port = console().ask_for_integer(
                "Please enter the SMTP server port associated with the email address",
                guard=lambda x: 0 < x < 65536,
            )

            flat_file().save_env(
                app_files().authelia_env,
                AUTHELIA_NOTIFIER_SMTP_HOST=smtp_host,
                AUTHELIA_NOTIFIER_SMTP_PORT=str(smtp_port),
                AUTHELIA_NOTIFIER_SMTP_USERNAME=email_address,
                AUTHELIA_NOTIFIER_SMTP_SENDER=f"{brand_name} <{email_address}>",
                AUTHELIA_NOTIFIER_SMTP_SUBJECT=f"[{brand_name}] {{title}}",
                AUTHELIA_SESSION_DOMAIN=domain_name,
            )

        if not app_files().authelia_smtp_password.exists():
            email_password = console().ask_for_password("Please enter the password for the email address")
            flat_file().save_secret(app_files().authelia_smtp_password, email_password)

        # Encryption key is used to encrypt the database, so we must create both
        if not app_files().authelia_encryption_key.exists() or not app_files().authelia_db.exists():
            console().print("Generating encryption key and database...")
            flat_file().create(app_files().authelia_db)
            flat_file().save_secret(app_files().authelia_encryption_key, generate_random_string())

        if not app_files().authelia_jwt_secret.exists():
            console().print("Generating JWT secret...")
            flat_file().save_secret(app_files().authelia_jwt_secret, generate_random_string())

        # Generate self-signed certificate
        if not app_files().nginx_cert.exists() or not app_files().nginx_key.exists():
            console().print("Generating self-signed certificate...")

            try:
                generate_self_signed_cert(app_files().nginx_cert, app_files().nginx_key)
            except Exception as e:
                console().print_error(f"Failed to generate self-signed certificate ({e}).")
                raise Exit(code=1)

        # Gather user information
        if not app_files().authelia_users.exists():
            console().print("No user information found. You will need to provide some information to continue.")

            users = []
            gather_user_info(users, usernames, full_names, emails, user_roles)
            users_file().save(users)

        console().request_for_newline()
        console().print("Initialization complete.")
    except Exception:
        # Remove existing configuration files if initialization fails
        reset_app()
        raise Exit(code=1)
