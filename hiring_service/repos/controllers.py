from abc import ABC, abstractmethod

from repos.models.candidate import Candidates, Candidate


class CandidateController(ABC):
    @abstractmethod
    def get_candidates(self) -> Candidates:
        raise NotImplementedError

    @abstractmethod
    def get_candidate(self, candidate_id: int) -> Candidate | None:
        raise NotImplementedError

    @abstractmethod
    def create_candidate(self, name: str, email: str) -> str | None:
        raise NotImplementedError
