from enum import auto, Enum


class EContainerService(str, Enum):
    NGINX = "nginx"
    KETO = "keto"
    KRATOS = "kratos"
    OATHKEEPER = "oathkeeper"
    NODE = "node"
    FILEBROWSER = "filebrowser"
    RSTUDIO = "rstudio"


class EContainerTool(Enum):
    DOCKER = auto()
    PODMAN = auto()
