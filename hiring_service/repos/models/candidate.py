from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Candidate:
    name: str
    email: str
    uuid: str


@dataclass(frozen=True)
class Candidates:
    candidates: list[Candidate]

    def __iter__(self) -> Iterator[Candidate]:
        return iter(self.candidates)


@dataclass(frozen=True)
class AssigmentExercise:
    exercise_uuid: str
    exercise_title: str
    exercise_text: str


@dataclass(frozen=True)
class AssigmentExercises:
    candidate: Candidate
    exercises: list[AssigmentExercise]
