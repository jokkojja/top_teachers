from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Optional


@dataclass(frozen=True)
class Exercise:
    uuid: str
    title: str
    text: str


@dataclass(frozen=True)
class Exercises:
    exercises: list[Exercise]

    def __iter__(self) -> Iterator[Exercise]:
        return iter(self.exercises)
