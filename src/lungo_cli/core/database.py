import os
from os import PathLike
from pathlib import Path

from typer import Exit

from .console import Console
from .constants import KETO_ADMIN_API_BASE_URL, KRATOS_ADMIN_API_BASE_URL
from .container import Container
from .file import FileUtils
from .network import HttpApiClient
from .storage import Storage
from ..helpers.common import format_input, format_path
from ..models.config import Privilege, Privileges
from ..models.users import Account


class AccountManager:
    def __init__(
        self, console: Console, file_utils: FileUtils, storage: Storage, client: HttpApiClient, container: Container
    ):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self.client = client
        self.container = container

    def verify(self, accounts: list[Account], user_dir: str | PathLike[str]) -> None:
        usernames = list(map(lambda x: x.username, accounts))

        if len(usernames) != len(set(usernames)):
            self.console.print_error("Username of each account must be unique.")
            raise Exit(code=1)

        for account in accounts:
            if account.username == "anonymous":
                self.console.print_warning(
                    f"Username {format_input('anonymous')} detected. "
                    "This account will be shared by all unregistered users when they access services "
                    "that require authentication. Please change the username if not intended."
                )

            if not (path := Path(user_dir).joinpath(account.username)).is_dir():
                if os.access(user_dir, os.W_OK):
                    self.console.print_info(f"Creating user directory at {format_path(path)}...")
                    self.file_utils.create_dir(path)
                else:
                    self.console.print_error(
                        f"User directory at {format_path(path)} does not exist. "
                        "Please create it with the appropriate permissions."
                    )
                    raise Exit(code=1)

    def update(self, accounts: list[Account], privileges: Privileges) -> None:
        self.container.up(self.storage.utils_keto_admin_dir)
        self.container.up(self.storage.utils_kratos_admin_dir)

        self.console.print_debug("Connecting to Keto Admin API...")
        self.client.ensure_reachable(f"{KETO_ADMIN_API_BASE_URL}/health/ready")

        # Remove all existing relation tuples
        self.console.print_debug("Removing existing relation tuples...")
        self.client.delete(f"{KETO_ADMIN_API_BASE_URL}/admin/relation-tuples?namespace=app")
        self.client.delete(f"{KETO_ADMIN_API_BASE_URL}/admin/relation-tuples?namespace=role")

        # Add base relation tuples
        data = [
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "app",
                    "object": "filebrowser",
                    "relation": "access",
                    "subject_set": {"namespace": "app", "object": "all", "relation": "access"},
                },
            },
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "app",
                    "object": "rstudio",
                    "relation": "access",
                    "subject_set": {"namespace": "app", "object": "all", "relation": "access"},
                },
            },
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "role",
                    "object": "unregistered",
                    "relation": "member",
                    "subject_set": {"namespace": "role", "object": "guest", "relation": "member"},
                },
            },
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "role",
                    "object": "guest",
                    "relation": "member",
                    "subject_set": {"namespace": "role", "object": "user", "relation": "member"},
                },
            },
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "role",
                    "object": "user",
                    "relation": "member",
                    "subject_set": {"namespace": "role", "object": "admin", "relation": "member"},
                },
            },
            {
                "action": "insert",
                "relation_tuple": {
                    "namespace": "role",
                    "object": "unregistered",
                    "relation": "member",
                    "subject_id": "anonymous",
                },
            },
        ]

        # Add role privileges
        for role in ["unregistered", "guest", "user", "admin"]:
            privilege: Privilege = getattr(privileges, role)

            if privilege.allowed_apps == "all":
                data.append(
                    {
                        "action": "insert",
                        "relation_tuple": {
                            "namespace": "app",
                            "object": "all",
                            "relation": "access",
                            "subject_set": {"namespace": "role", "object": role, "relation": "member"},
                        },
                    },
                )
            else:
                for allowed_app in privilege.allowed_apps:
                    data.append(
                        {
                            "action": "insert",
                            "relation_tuple": {
                                "namespace": "app",
                                "object": allowed_app.value,
                                "relation": "access",
                                "subject_set": {"namespace": "role", "object": role, "relation": "member"},
                            },
                        },
                    )

        # Add account privileges
        for account in accounts:
            data.append(
                {
                    "action": "insert",
                    "relation_tuple": {
                        "namespace": "role",
                        "object": account.role.value,
                        "relation": "member",
                        "subject_id": account.username,
                    },
                },
            )

            if account.extra.allowed_apps == "all":
                data.append(
                    {
                        "action": "insert",
                        "relation_tuple": {
                            "namespace": "app",
                            "object": "all",
                            "relation": "access",
                            "subject_id": account.username,
                        },
                    },
                )
            else:
                for allowed_app in account.extra.allowed_apps:
                    data.append(
                        {
                            "action": "insert",
                            "relation_tuple": {
                                "namespace": "app",
                                "object": allowed_app.value,
                                "relation": "access",
                                "subject_id": account.username,
                            },
                        },
                    )

        self.console.print_debug("Creating new relation tuples...")
        self.client.patch(f"{KETO_ADMIN_API_BASE_URL}/admin/relation-tuples", data)

        self.container.down(self.storage.utils_keto_admin_dir)

        self.console.print_debug("Connecting to Kratos Admin API...")
        self.client.ensure_reachable(f"{KRATOS_ADMIN_API_BASE_URL}/health/ready")

        accounts = accounts[:]

        for old_account in self.client.get(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities"):
            if new_account := next(filter(lambda x: x.username == old_account["traits"]["username"], accounts), None):
                # Update the account
                accounts.remove(new_account)
                data = []

                if old_account["state"] != (state := ("active" if new_account.enabled else "inactive")):
                    data.append({"op": "replace", "path": "/state", "value": state})
                if old_account["traits"]["email"] != new_account.email:
                    data.append({"op": "replace", "path": "/traits/email", "value": new_account.email})
                if old_account["traits"]["name"]["first"] != new_account.name.first:
                    data.append({"op": "replace", "path": "/traits/name/first", "value": new_account.name.first})
                if old_account["traits"]["name"]["last"] != new_account.name.last:
                    data.append({"op": "replace", "path": "/traits/name/last", "value": new_account.name.last})

                if data:
                    self.console.print_debug(f"Updating account {format_input(new_account.username)}...")
                    self.client.patch(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities/{old_account['id']}", data)
            else:
                # Remove the account
                self.console.print_debug(f"Removing account {format_input(old_account['traits']['username'])}...")
                self.client.delete(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities/{old_account['id']}")

        for new_account in accounts:
            # Create the account
            data = {
                "schema_id": "user",
                "state": "active" if new_account.enabled else "inactive",
                "traits": {
                    "username": new_account.username,
                    "email": new_account.email,
                    "name": {"first": new_account.name.first, "last": new_account.name.last},
                },
            }

            self.console.print_debug(f"Creating account {format_path(new_account.username)}...")
            self.client.post(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities", data)

        self.container.down(self.storage.utils_kratos_admin_dir)
