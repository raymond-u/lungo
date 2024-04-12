from typing import Annotated, Final, Literal

from aenum import auto, StrEnum
from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, use_enum_values=True)


class EApp(StrEnum):
    pass


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


AllowedAppsType: Final = Literal["all"] | list[EApp]
FileNameType: Final = Annotated[str, Field(pattern=r"^[a-zA-Z0-9._-]+$")]
NameStrType: Final = Annotated[str, Field(max_length=32)]
PortType: Final = Annotated[int, Field(ge=1, le=65535)]
UsernameType: Final = Annotated[str, Field(pattern=r"^[a-z_](?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$")]
