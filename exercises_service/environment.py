from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from typing import Callable, TypeVar, Self

from dotenv import load_dotenv


load_dotenv()

T = TypeVar("T")


@dataclass(frozen=True)
class Config(ABC):
    @classmethod
    @abstractmethod
    def from_env(cls) -> Self:
        raise NotImplementedError


@dataclass(frozen=True)
class EnvVar:
    @classmethod
    def get_required(cls, key: str, from_str: Callable[[str], T] = str) -> T:
        variable = os.getenv(key)
        if variable is None:
            raise KeyError(f"Environment variable not found: {key}")

        return from_str(variable)

    @classmethod
    def get_or_default(
        cls, key: str, default: T, from_str: Callable[[str], T] = str
    ) -> T:
        variable = os.getenv(key)
        if variable is None:
            return default

        return from_str(variable)
