from abc import ABC, abstractmethod

from repos.models.candidate import Candidates, Candidate


class ExerciseController(ABC):
    @abstractmethod
    def create_exercise(
        self, exercise_uuid: str, exercise_title: str, exercise_text: str
    ) -> int:
        raise NotImplementedError


class CandidateController(ABC):
    @abstractmethod
    def get_candidates(self) -> Candidates | None:
        raise NotImplementedError

    @abstractmethod
    def get_candidate(self, candidate_id: int) -> Candidate | None:
        raise NotImplementedError

    @abstractmethod
    def create_candidate(self, name: str, email: str) -> str | None:
        raise NotImplementedError
