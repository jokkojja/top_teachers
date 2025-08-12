from contextlib import contextmanager
from typing import Iterator, Self

from psycopg2.extensions import cursor as PsycopgCursor
from psycopg2.pool import ThreadedConnectionPool

from repos.config import PostgreConfig
from repos.repo import Repo


class Postgre(Repo):
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
    def conn(self) -> Iterator[PsycopgCursor]:
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

    def create_exercise(self):
        with self.conn() as conn:
            pass

    def update_exercise(self):
        with self.conn() as conn:
            pass

    def create_manager(self):
        with self.conn() as conn:
            pass

    def create_admin(self):
        with self.conn() as conn:
            pass
