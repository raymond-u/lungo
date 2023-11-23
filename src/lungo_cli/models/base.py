from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, use_enum_values=True)


class EApp(str, Enum):
    FILEBROWSER = "filebrowser"
    JUPYTERHUB = "jupyterhub"
    PRIVATEBIN = "privatebin"
    RSTUDIO = "rstudio"
    XRAY = "xray"


class EContainer(str, Enum):
    DOCKER = "docker"
    DOCKER_COMPOSE = "docker-compose"
    PODMAN_COMPOSE = "podman-compose"


class EService(str, Enum):
    NGINX_GATEWAY = "nginx_gateway"
    NGINX = "nginx"
    KETO = "keto"
    KRATOS = "kratos"
    OATHKEEPER = "oathkeeper"
    NODE = "node"
    FILEBROWSER = "filebrowser"
    JUPYTERHUB = "jupyterhub"
    PRIVATEBIN = "privatebin"
    RSTUDIO = "rstudio"
    XRAY = "xray"


class ERole(str, Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


AllowedApps = Literal["all"] | list[EApp]
FileName = Annotated[str, Field(pattern=r"^[a-zA-Z0-9._-]+$")]
NameStr = Annotated[str, Field(max_length=32)]
Port = Annotated[int, Field(ge=1, le=65535)]
Username = Annotated[str, Field(pattern=r"^[a-z_](?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$")]
