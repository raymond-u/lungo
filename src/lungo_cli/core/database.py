from .console import Console
from .constants import KETO_ADMIN_API_BASE_URL, KRATOS_ADMIN_API_BASE_URL
from .container import Container
from .file import FileUtils
from .network import HttpApiClient
from .storage import Storage
from ..helpers.format import format_input, format_path
from ..models.base import EApp
from ..models.config import Config, Privilege
from ..models.users import Users


class AccountManager:
    """Validate and update user accounts."""

    def __init__(
        self, client: HttpApiClient, console: Console, container: Container, file_utils: FileUtils, storage: Storage
    ):
        self.client = client
        self.console = console
        self.container = container
        self.file_utils = file_utils
        self.storage = storage

    def update(self, config: Config, users: Users, app_web_path_map: dict[str, str]) -> None:
        # Ensure that the container can always be started even if it failed last time
        self.console.print_info("Updating user accounts...")

        self.container.down(self.storage.service_keto_admin_dir)
        self.container.down(self.storage.service_kratos_admin_dir)

        self.container.up(self.storage.service_keto_admin_dir)
        self.container.up(self.storage.service_kratos_admin_dir)

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

        enabled_apps = []

        app: EApp
        for app in EApp:
            if getattr(config.plugins, app.value).enabled:
                enabled_apps.append(app)
                data.append(
                    {
                        "action": "insert",
                        "relation_tuple": {
                            "namespace": "app",
                            "object": app_web_path_map[app.value],
                            "relation": "access",
                            "subject_set": {"namespace": "app", "object": "all", "relation": "access"},
                        },
                    }
                )

        # Add role privileges
        for role in ["unregistered", "guest", "user", "admin"]:
            privilege: Privilege = getattr(config.rules.privileges, role)

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
                    # Pydantic does not distinguish between a string and an enum value
                    if type(allowed_app) is str:
                        allowed_app = EApp(allowed_app)

                    if allowed_app in enabled_apps:
                        data.append(
                            {
                                "action": "insert",
                                "relation_tuple": {
                                    "namespace": "app",
                                    "object": app_web_path_map[allowed_app.value],
                                    "relation": "access",
                                    "subject_set": {"namespace": "role", "object": role, "relation": "member"},
                                },
                            },
                        )

        # Add account privileges
        for account in users.accounts:
            # Anonymous account is covered by base relation tuples
            if account.username != "anonymous":
                data.append(
                    {
                        "action": "insert",
                        "relation_tuple": {
                            "namespace": "role",
                            "object": account.role if type(account.role) is str else account.role.value,
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
                    # Pydantic does not distinguish between a string and an enum value
                    if type(allowed_app) is str:
                        allowed_app = EApp(allowed_app)

                    if allowed_app in enabled_apps:
                        data.append(
                            {
                                "action": "insert",
                                "relation_tuple": {
                                    "namespace": "app",
                                    "object": app_web_path_map[allowed_app.value],
                                    "relation": "access",
                                    "subject_id": account.username,
                                },
                            },
                        )

        self.console.print_debug("Creating new relation tuples...")
        self.client.patch(f"{KETO_ADMIN_API_BASE_URL}/admin/relation-tuples", data)

        self.container.down(self.storage.service_keto_admin_dir)

        self.console.print_debug("Connecting to Kratos Admin API...")
        self.client.ensure_reachable(f"{KRATOS_ADMIN_API_BASE_URL}/health/ready")

        accounts = users.accounts[:]

        # It makes no sense for the anonymous account to be managed by Kratos
        if anonymous_account := next(filter(lambda x: x.username == "anonymous", accounts), None):
            accounts.remove(anonymous_account)

        # This endpoint by default returns the first 250 accounts, but should be enough for most use cases
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
                    self.client.patch(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities/{old_account["id"]}", data)
            else:
                # Remove the account
                self.console.print_debug(f"Removing account {format_input(old_account["traits"]["username"])}...")
                self.client.delete(f"{KRATOS_ADMIN_API_BASE_URL}/admin/identities/{old_account["id"]}")

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

        self.container.down(self.storage.service_kratos_admin_dir)
