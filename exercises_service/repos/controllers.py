from abc import ABC, abstractmethod
from datetime import datetime

from repos.models.exercise import Exercise
from repos.models.user import User, Users


class UserController(ABC):
    @abstractmethod
    def get_users(self) -> Users:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, name: str, role: str) -> int:
        raise NotImplementedError


class ExercisesController(ABC):
    @abstractmethod
    def create_exercise(self, title: str, text: str, author_id: int) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def get_exercise(self, exercise_id: int) -> Exercise | None:
        raise NotImplementedError

    @abstractmethod
    def update_exercise(
        self, exercise_id: int, text: str, updated_at: datetime
    ) -> str | None:
        raise NotImplementedError
