import platform
from typing import Final

APP_NAME: Final = "lungo"
APP_NAME_CAPITALIZED: Final = APP_NAME.capitalize()
APP_AUTHOR: Final = APP_NAME
PACKAGE_NAME: Final = "lungo_cli"

STORAGE_PREFIX: Final = "v"
STORAGE_VERSION: Final = "v0"

PLUGIN_WEB_ENTRYPOINT: Final = "app"

OPENRESTY_VERSION: Final = "1.25.3.1-alpine-apk"
KETO_VERSION: Final = "v0.12.0"
KRATOS_VERSION: Final = "v1.1.0"
OATHKEEPER_VERSION: Final = "v0.40.7"
NODE_VERSION: Final = "20.14.0-alpine"

KETO_ADMIN_API_BASE_URL: Final = "http://127.0.0.1:3939"
KRATOS_ADMIN_API_BASE_URL: Final = "http://127.0.0.1:3940"

DOCKER_URL: Final = "https://www.docker.com/"
DOCKER_COMPOSE_URL: Final = "https://github.com/docker/compose"
PODMAN_URL: Final = "https://podman.io/"
PODMAN_COMPOSE_URL: Final = "https://github.com/containers/podman-compose"

match platform.machine():
    case "aarch64" | "arm64":
        ARCHITECTURE: Final = "aarch64"
    case "amd64" | "x86_64":
        ARCHITECTURE: Final = "x86_64"
    case _:
        ARCHITECTURE: Final = platform.machine()
