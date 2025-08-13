from contextlib import contextmanager
import hashlib
import secrets
import string
from typing import Iterator, Self

from psycopg2.extensions import cursor as PsycopgCursor
from psycopg2.pool import ThreadedConnectionPool

from repos.config import PostgreConfig
from repos.models.user import User, Users
from repos.repo import Repo


def generate_token(name: str, role: str) -> str:
    """Генерирует уникальный токен с солью."""
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    raw = f"{name}{role}{salt}".encode()
    return hashlib.sha256(raw).hexdigest()


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

    def get_users(self) -> Users:
        with self.conn() as conn:
            conn.execute(
                "SELECT u.name, r.role, u.token from users as u join roles as r on u.role_id = r.id"
            )
            users = conn.fetchall()
            return Users(
                users=[User(name=user[0], role=user[1], hash=user[2])
                       for user in users]
            )

    def get_user(self, user_id: int) -> User | None:
        with self.conn() as conn:
            conn.execute(
                "SELECT u.name, r.role, u.token from users as u join roles as r on u.role_id = r.id where u.id=%s",
                (user_id,),
            )
            user = conn.fetchone()
            if user is None:
                return
            return User(name=user[0], role=user[1], hash=user[2])

    def create_exercise(self):
        with self.conn() as conn:
            pass

    def update_exercise(self):
        with self.conn() as conn:
            pass

    def create_user(self, name: str, role: str) -> int:
        with self.conn() as conn:
            get_role_query = "SELECT id FROM roles WHERE role = %s"
            conn.execute(get_role_query, (role,))
            role_data = conn.fetchone()
            role_id = role_data[0]

            insert_query = """
                INSERT INTO users (name, role_id, token)
                VALUES (%s, %s, %s)
                RETURNING id
            """

            token = generate_token(name, role)
            conn.execute(
                insert_query,
                (name, role_id, token),
            )
            user_id = conn.fetchone()[0]
            return user_id
