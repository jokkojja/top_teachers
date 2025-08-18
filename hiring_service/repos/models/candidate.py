from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Candidate:
    name: str
    email: str


@dataclass(frozen=True)
class Candidates:
    candidates: list[Candidate]

    def __iter__(self) -> Iterator[Candidate]:
        return iter(self.candidates)
