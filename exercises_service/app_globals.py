from dataclasses import dataclass
from typing import Self

from repos.postgre import Postgre


@dataclass(frozen=True)
class DatabaseSession:
    postgres: Postgre

    @classmethod
    def from_env(cls) -> Self:
        postgre = Postgre.from_env()
        return cls(postgre)


@dataclass(frozen=True)
class AppGlobals:
    database_session: DatabaseSession

    @classmethod
    async def create(cls) -> Self:
        database_session = DatabaseSession.from_env()
        return cls(database_session)
