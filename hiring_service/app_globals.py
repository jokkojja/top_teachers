from dataclasses import dataclass
from typing import Self

from repos.postgre import PostgreCandidateController


@dataclass(frozen=True)
class PostgreControllers:
    candidate_controller: PostgreCandidateController

    @classmethod
    def from_env(cls) -> Self:
        candidate_controller = PostgreCandidateController.from_env()

        return cls(candidate_controller)


@dataclass(frozen=True)
class AppGlobals:
    postgre_controllers: PostgreControllers

    @classmethod
    async def create(cls) -> Self:
        database_session = PostgreControllers.from_env()
        return cls(database_session)
