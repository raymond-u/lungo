from ipaddress import IPv4Network
from os import PathLike
from pathlib import Path

from importlib_resources import as_file, files
from typer import Exit

from .common import format_input, format_path
from .crypto import generate_random_string, generate_self_signed_cert
from .yaml import parse_yaml
from ..app.state import account_manager, console, file_utils, renderer, storage
from ..core.constants import PACKAGE_NAME
from ..models.config import Config
from ..models.context import AppDirs, Context, IpAddresses
from ..models.users import Users


def process_args(config_dir: str | PathLike[str] | None, quiet: bool, verbosity: int) -> None:
    """Process common arguments."""
    if config_dir:
        if not Path(config_dir).is_dir():
            console().print_error(f"{format_path(config_dir)} is not a directory.")
            raise Exit(code=1)

        storage().config_dir = Path(config_dir).resolve()

    if quiet:
        console().set_log_level(-1)
    else:
        console().set_log_level(verbosity)


def process_args_delayed(dev: bool, force_init: bool = False, remove_lock: bool = False) -> None:
    """Process common arguments that need to be processed after the configuration is loaded."""
    if dev:
        storage().storage_version = "dev"
        console().set_log_level(1)

    if force_init:
        file_utils().remove(storage().bundled_dir)

    if remove_lock:
        file_utils().remove(storage().lock_file)


def copy_resources(src: str | PathLike[str], dst: str | PathLike[str]) -> None:
    """Copy resources from the package to the destination directory."""
    with as_file(files(f"{PACKAGE_NAME}.resources")) as resources:
        file_utils().copy(resources / src, dst)


def get_ip_addresses(subnet: str | IPv4Network) -> IpAddresses:
    """Get the IP addresses for the services."""
    subnet = IPv4Network(subnet)

    if subnet.num_addresses < 256:
        console().print_error(
            f"Subnet {format_input(str(subnet))} is too small. "
            "Please change it to a subnet with at least 256 addresses."
        )
        raise Exit(code=1)

    hosts = list(subnet.hosts())

    return IpAddresses(
        nginx=hosts[100],
        keto=hosts[101],
        kratos=hosts[102],
        oathkeeper=hosts[103],
        node=hosts[104],
        filebrowser=hosts[105],
        rstudio=hosts[106],
    )


def create_context(config: Config, users: Users) -> Context:
    """Create a context object for template rendering."""
    app_dirs = AppDirs(
        cache_dir=storage().cache_latest_dir,
        generated_dir=storage().generated_dir,
        managed_dir=storage().managed_dir,
    )

    return Context(
        config=config,
        users=users,
        app_dirs=app_dirs,
        ip_addresses=get_ip_addresses(config.network.subnet),
        rstudio_password=file_utils().read_text(storage().rstudio_password_file),
    )


def ensure_application_data(config: Config, users: Users) -> None:
    """Ensure that all the application data exists and is up-to-date."""
    with console().status("Updating storage..."):
        storage().validate()
        storage().create_dirs()

        if not storage().bundled_dir.is_dir() or storage().storage_version == "dev":
            console().print_info("Updating bundled data...")
            copy_resources(".", storage().bundled_dir)
            file_utils().remove(storage().init_file)

        if not storage().nginx_cert_file.is_file() or not storage().nginx_key_file.is_file():
            console().print_info("Generating self-signed certificate...")
            cert, key = generate_self_signed_cert()
            file_utils().write_bytes(storage().nginx_cert_file, cert)
            file_utils().write_bytes(storage().nginx_key_file, key)

        if not storage().kratos_secrets_file.is_file():
            console().print_info("Generating Kratos secrets...")
            renderer().render(
                storage().template_kratos_secrets_rel,
                storage().kratos_secrets_file,
                secret_cookie=generate_random_string(),
            )

        if not storage().rstudio_password_file.is_file():
            console().print_info("Generating RStudio password...")
            file_utils().write_text(storage().rstudio_password_file, generate_random_string())

    with console().status("Updating database..."):
        config_hash = hash_config()

        if not storage().init_file.is_file() or file_utils().read_text(storage().init_file) != config_hash:
            file_utils().remove(storage().init_file)

            renderer().render_all(create_context(config, users))
            account_manager().verify(config, users)
            account_manager().update(config, users)

            file_utils().write_text(storage().init_file, config_hash)


def hash_config() -> str:
    """Hash the configuration files."""
    return file_utils().hash_sha256(storage().config_file) + file_utils().hash_sha256(storage().users_file)


def load_config() -> tuple[Config, Users]:
    """Load the configuration files and may set application directories."""
    if not storage().config_file.is_file():
        console().print_error(
            f"{format_path(storage().config_file.name)} not found. "
            "A template will be created, please read the manual to learn how to configure it."
        )
        copy_resources(storage().template_config_rel, storage().config_file)

        raise Exit(code=1)

    if not storage().users_file.is_file():
        console().print_error(
            f"{format_path(storage().users_file.name)} not found. "
            "A template will be created, please read the manual to learn how to configure it."
        )
        copy_resources(storage().template_users_rel, storage().users_file)

        raise Exit(code=1)

    config = parse_yaml(storage().config_file, Config)
    users = parse_yaml(storage().users_file, Users)

    if config.directories.cache_dir:
        storage().cache_dir = config.directories.cache_dir.resolve()
    if config.directories.data_dir:
        storage().data_dir = config.directories.data_dir.resolve()

    return config, users
