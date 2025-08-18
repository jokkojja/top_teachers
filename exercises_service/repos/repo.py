from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator, Self


class Repo(ABC):
    @abstractmethod
    @contextmanager
    def _conn(self) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_env(cls) -> Self:
        raise NotImplementedError
