from typing import Self

import psycopg2

from repos.repo import Repo


class PostgreRepo(Repo):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_env() -> Self:
        pass

    def create_exercise(self):
        pass

    def update_exercise(self):
        pass
