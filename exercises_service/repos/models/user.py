from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class User:
    name: str
    role: str


@dataclass(frozen=True)
class Users:
    users: list[User]

    def __iter__(self) -> Iterator[User]:
        return iter(self.users)
