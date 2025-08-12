from dataclasses import dataclass
from typing import TypedDict

from api.models.roles import Role


@dataclass(frozen=True)
class User:
    name: str
    role: Role


@dataclass(frozen=True)
class Users:
    users: list[User]
