from typing import Final

APP_NAME: Final[str] = "lungo"
APP_NAME_CAPITALIZED: Final[str] = APP_NAME.capitalize()
APP_AUTHOR: Final[str] = APP_NAME
PACKAGE_NAME: Final[str] = "lungo_cli"

DOCKER_URL: Final[str] = "https://www.docker.com/"
PODMAN_URL: Final[str] = "https://podman.io/"
PODMAN_COMPOSE_URL: Final[str] = "https://github.com/containers/podman-compose"

AUTHELIA_DEFAULT_PASSWORD: Final[str] = "passwd"
AUTHELIA_DEFAULT_PASSWORD_HASH: Final[str] = ("$6$rounds=50000$.6eb7g/OiBTWqobG$TiZFd6cDWAVkamdL4ww1AGGcAoy"
                                              "SkQI9rdrRQMz3XUrufcrJaAM/IJC4ZZtAXU8HNWQfphI/9wtqMPyuENlD80")
FILEBROWSER_DEFAULT_PASSWORD_HASH: Final[str] = "$2a$10$aulj1r/ROe0VnA1iE2/ojOItBBFeHK0KLMv5mnl3ECXfiNLKfcKHi"
