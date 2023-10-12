from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, use_enum_values=True)


class EApp(str, Enum):
    FILEBROWSER = "filebrowser"
    RSTUDIO = "rstudio"


class ERole(str, Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


AllowedApps = Literal["all"] | list[EApp]
Port = Annotated[int, Field(ge=1, le=65535)]
Username = Annotated[str, Field(pattern=r"^[a-z_](?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$")]
