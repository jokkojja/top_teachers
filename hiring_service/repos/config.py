from dataclasses import dataclass
from typing import Self

from environment import EnvVar, Config


@dataclass(frozen=True)
class PostgreConfig(Config):
    host: str
    port: str
    user: str
    password: str
    database: str

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @classmethod
    def from_env(cls) -> Self:
        host = EnvVar.get_required(key="PG_HOST")
        port = EnvVar.get_required(key="PG_PORT")
        user = EnvVar.get_required(key="PG_USER")
        password = EnvVar.get_required(key="PG_PASSWORD")
        database = EnvVar.get_required(key="PG_DATABASE")
        return cls(host, port, user, password, database)
