from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Assigment:
    id: int
    candidate_uuid: str
    exercise_uuid: str


@dataclass(frozen=True)
class Assigments:
    assigments: list[Assigment]

    def __iter__(self) -> Iterator[Assigment]:
        return iter(self.assigments)
