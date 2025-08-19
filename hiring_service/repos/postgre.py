from contextlib import contextmanager
from datetime import datetime
import hashlib
import secrets
import string
from typing import Final, Iterator, Self
from uuid import UUID

from psycopg2.extensions import cursor as PsycopgCursor
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.errors import ForeignKeyViolation

from repos.config import PostgreConfig
from repos.controllers import CandidateController
from repos.models.candidate import Candidate, Candidates
from repos.repo import Repo


def generate_token(encode_string: str) -> str:
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    raw = f"{encode_string}{salt}".encode()
    return hashlib.sha256(raw).hexdigest()


class Postgre(Repo):
    _EXERCISE_TABLE: Final[str] = "exercises"
    _CANDIDATES_TABLE: Final[str] = "candidates"
    _ASSIGMENTS_TABLE: Final[str] = "assignments"

    def __init__(
        self,
        config: PostgreConfig,
        min_connections: int = 1,
        max_connections: int = 10,
    ) -> None:
        self.__pool = ThreadedConnectionPool(
            dsn=config.dsn, minconn=min_connections, maxconn=max_connections
        )

    @contextmanager
    def _conn(self) -> Iterator[PsycopgCursor]:
        conn = self.__pool.getconn()
        try:
            with conn:
                with conn.cursor() as cursor:
                    yield cursor
        finally:
            self.__pool.putconn(conn)

    def close(self) -> None:
        self.__pool.closeall()

    @classmethod
    def from_env(cls) -> Self:
        config = PostgreConfig.from_env()
        return cls(config)


class PostgreCandidateController(CandidateController):
    def __init__(self, config: PostgreConfig) -> None:
        self.repo = Postgre(config=config)

    @classmethod
    def from_env(cls) -> Self:
        config = PostgreConfig.from_env()
        return cls(config)

    def get_candidates(self) -> Candidates:
        with self.repo._conn() as conn:
            conn.execute(f"SELECT name, email from {self.repo._CANDIDATES_TABLE}")
            candidates = conn.fetchall()
            return Candidates(
                candidates=[
                    Candidate(name=candidate[0], email=candidate[1])
                    for candidate in candidates
                ]
            )

    def get_candidate(self, candidate_id: int) -> Candidate | None:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT name, email from {self.repo._CANDIDATES_TABLE} where id=%s""",
                (candidate_id,),
            )
            exercise = conn.fetchone()
            if exercise is None:
                return

            return Candidate(
                name=exercise[0],
                email=exercise[1],
            )

    def create_candidate(self, name: str, email: str) -> str | None:
        with self.repo._conn() as conn:
            insert_query = f"""
                INSERT INTO {self.repo._CANDIDATES_TABLE} (name, email)
                VALUES (%s, %s)
                RETURNING uuid
            """
            conn.execute(
                insert_query,
                (
                    name,
                    email,
                ),
            )

            candidate = conn.fetchone()
            if candidate is None:
                return

            return candidate[0]
