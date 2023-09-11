from enum import auto, Enum


class ContainerService(str, Enum):
    """Container services."""

    AUTHELIA = "authelia"
    FILEBROWSER = "filebrowser"
    NGINX = "nginx"
    RSTUDIO = "rstudio"


class ContainerTool(Enum):
    """Container management tools."""

    DOCKER = auto()
    PODMAN = auto()
