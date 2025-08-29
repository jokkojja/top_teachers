from abc import ABC, abstractmethod
from datetime import datetime

from repos.models.exercise import Exercise
from repos.models.user import User, Users
from repos.models.candidate import Candidates


class CandidateController(ABC):
    @abstractmethod
    def create_candidate(self, candidate_uuid: str, candidate_name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_candidates(self) -> Candidates | None:
        raise NotImplementedError


class UserController(ABC):
    @abstractmethod
    def get_users(self) -> Users | None:
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

    @abstractmethod
    def assign_exercise(self, candidate_uuid: str, exercise_uuid: str) -> bool:
        raise NotImplementedError
