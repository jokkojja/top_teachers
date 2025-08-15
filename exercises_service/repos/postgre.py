from contextlib import contextmanager
from datetime import datetime
import hashlib
import secrets
import string
from typing import Final, Iterator, Self

from psycopg2.extensions import cursor as PsycopgCursor
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.errors import ForeignKeyViolation

from repos.config import PostgreConfig
from repos.controllers import ExercisesController, UserController
from repos.models.user import User, Users
from repos.models.exercise import Exercise
from repos.repo import Repo


def generate_token(encode_string: str) -> str:
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    raw = f"{encode_string}{salt}".encode()
    return hashlib.sha256(raw).hexdigest()


class Postgre(Repo):
    _EXERCISE_TABLE: Final[str] = "exercises"
    _ROLES_TABLE: Final[str] = "roles"
    _USERS_TABLE: Final[str] = "users"
    _CADIDATES_TABLE: Final[str] = "candidates"
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


class PostgreExercisesController(ExercisesController):
    def __init__(self, config: PostgreConfig) -> None:
        self.repo = Postgre(config=config)

    @classmethod
    def from_env(cls) -> Self:
        config = PostgreConfig.from_env()
        return cls(config)

    def create_exercise(self, title: str, text: str, author_id: int) -> int | None:
        with self.repo._conn() as conn:
            insert_query = f"""
                INSERT INTO {self.repo._EXERCISE_TABLE} (title, text, author_id)
                VALUES (%s, %s, %s)
                RETURNING id
            """
            try:
                conn.execute(
                    insert_query,
                    (title, text, author_id),
                )
            except ForeignKeyViolation:
                return None

            exercise_id = conn.fetchone()[0]
            return exercise_id

    def get_exercise(self, exercise_id: int) -> Exercise | None:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT id, title, text, author_id, uuid, created_at, updated_at from {
                    self.repo._EXERCISE_TABLE
                } where id=%s""",
                (exercise_id,),
            )
            exercise = conn.fetchone()
            if exercise is None:
                return
            return Exercise(
                exercise_id=exercise[0],
                title=exercise[1],
                text=exercise[2],
                author_id=exercise[3],
                uuid=exercise[4],
                created_at=exercise[5],
                updated_at=exercise[6],
            )

    def update_exercise(
        self, exercise_id: int, text: str, updated_at: datetime
    ) -> bool:
        with self.repo._conn() as conn:
            conn.execute(
                f"""UPDATE {
                    self.repo._EXERCISE_TABLE
                } SET text=%s, updated_at=%s where id=%s RETURNING id""",
                (
                    text,
                    updated_at,
                    exercise_id,
                ),
            )
            return conn.fetchone() is not None


class PostgreUserContoller(UserController):
    def __init__(self, config: PostgreConfig) -> None:
        self.repo = Postgre(config=config)

    @classmethod
    def from_env(cls) -> Self:
        config = PostgreConfig.from_env()
        return cls(config)

    def get_users(self) -> Users:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT u.name, r.role, u.token from {
                    self.repo._USERS_TABLE
                } as u join roles as r on u.role_id = r.id"""
            )
            users = conn.fetchall()
            return Users(
                users=[User(name=user[0], role=user[1], hash=user[2]) for user in users]
            )

    def get_user(self, user_id: int) -> User | None:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT u.name, r.role, u.token from {
                    self.repo._USERS_TABLE
                } as u join roles as r on u.role_id = r.id where u.id=%s""",
                (user_id,),
            )
            user = conn.fetchone()
            if user is None:
                return
            return User(name=user[0], role=user[1], hash=user[2])

    def create_user(self, name: str, role: str) -> int:
        with self.repo._conn() as conn:
            get_role_query = (
                f"""SELECT id FROM {self.repo._ROLES_TABLE} WHERE role = %s"""
            )
            conn.execute(get_role_query, (role,))
            role_data = conn.fetchone()
            role_id = role_data[0]

            insert_query = f"""
                INSERT INTO {self.repo._USERS_TABLE} (name, role_id, token)
                VALUES (%s, %s, %s)
                RETURNING id
            """
            encode_string = f"{name}{role}"
            token = generate_token(encode_string)
            conn.execute(
                insert_query,
                (name, role_id, token),
            )
            user_id = conn.fetchone()[0]
            return user_id
