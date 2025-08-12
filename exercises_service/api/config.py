from dataclasses import dataclass
from typing import Self

from environment import EnvVar, Config
from logs import LogLevel


@dataclass(frozen=True)
class ApiConfig(Config):
    port: int
    log_level: str

    @classmethod
    def from_env(cls) -> Self:
        port = EnvVar.get_required(key="PORT", from_str=int)
        log_level = LogLevel.from_str(
            EnvVar.get_or_default(key="LOG_LEVEL", default=LogLevel.Info)
        ).value
        return cls(port, log_level)
