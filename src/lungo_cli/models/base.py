from typing import Annotated, Literal

from aenum import auto, StrEnum
from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, use_enum_values=True)


class EApp(StrEnum): ...


class EContainer(StrEnum):
    DOCKER = auto()
    DOCKER_COMPOSE = "docker-compose"
    PODMAN_COMPOSE = "podman-compose"


class ECoreService(StrEnum):
    NGINX_GATEWAY = auto()
    NGINX = auto()
    KETO = auto()
    KRATOS = auto()
    OATHKEEPER = auto()
    NODE = auto()


class ERole(StrEnum):
    GUEST = auto()
    USER = auto()
    ADMIN = auto()


AllowedApps = Literal["all"] | list[EApp]
FileName = Annotated[str, Field(pattern=r"^[a-zA-Z0-9._-]+$")]
NameStr = Annotated[str, Field(max_length=32)]
Port = Annotated[int, Field(ge=1, le=65535)]
Username = Annotated[str, Field(pattern=r"^[a-z_](?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$")]
