from dataclasses import dataclass
from typing import Self

from repos.postgre import Postgre, PostgreExercisesController, PostgreUserContoller


@dataclass(frozen=True)
class PostgreControllers:
    users_controller: PostgreUserContoller
    exercises_controller: PostgreExercisesController

    @classmethod
    def from_env(cls) -> Self:
        users_controller = PostgreUserContoller.from_env()
        exercises_controller = PostgreExercisesController.from_env()
        return cls(users_controller, exercises_controller)


@dataclass(frozen=True)
class AppGlobals:
    postgre_controllers: PostgreControllers

    @classmethod
    async def create(cls) -> Self:
        database_session = PostgreControllers.from_env()
        return cls(database_session)
