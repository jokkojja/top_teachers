from dataclasses import dataclass
import os
from typing import Callable, TypeVar, Self

from dotenv import load_dotenv

from logs import LogLevel

load_dotenv()

T = TypeVar("T")


@dataclass(frozen=True)
class ApiConfig:
    port: int
    log_level: str

    @classmethod
    def from_env(cls) -> Self:
        port = EnvVar.get_required(key="PORT", from_str=int)
        log_level = LogLevel.from_str(
            EnvVar.get_or_default(key="LOG_LEVEL", default=LogLevel.Info)
        ).value
        return cls(port, log_level)


@dataclass(frozen=True)
class EnvVar:
    @classmethod
    def get_required(cls, key: str, *, from_str: Callable[[str], T] = str) -> T:
        variable = os.getenv(key)
        if variable is None:
            raise KeyError(f"Environment variable not found: {key}")

        return from_str(variable)

    @classmethod
    def get_or_default(
        cls, key: str, default: T, *, from_str: Callable[[str], T] = str
    ) -> T:
        variable = os.getenv(key)
        if variable is None:
            return default

        return from_str(variable)
