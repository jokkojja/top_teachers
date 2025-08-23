from contextlib import contextmanager
from typing import Final, Iterator, Self

from psycopg2.errors import ForeignKeyViolation
from psycopg2.extensions import cursor as PsycopgCursor
from psycopg2.pool import ThreadedConnectionPool

from repos.config import PostgreConfig
from repos.controllers import ExerciseController, CandidateController
from repos.models.candidate import (
    Candidate,
    Candidates,
    AssigmentExercise,
    AssigmentExercises,
)
from repos.models.exercises import Exercises, Exercise
from repos.repo import Repo


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
            conn.execute(
                f"""SELECT name, email, uuid from {self.repo._CANDIDATES_TABLE}"""
            )
            candidates = conn.fetchall()
            return Candidates(
                candidates=[
                    Candidate(name=candidate[0], email=candidate[1], uuid=candidate[2])
                    for candidate in candidates
                ]
            )

    def get_candidate(self, candidate_id: int) -> Candidate | None:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT name, email, uuid from {
                    self.repo._CANDIDATES_TABLE
                } where id=%s""",
                (candidate_id,),
            )
            exercise = conn.fetchone()
            if exercise is None:
                return

            return Candidate(name=exercise[0], email=exercise[1], uuid=exercise[2])

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


class PostgreExerciseController(ExerciseController):
    def __init__(self, config: PostgreConfig) -> None:
        self.repo = Postgre(config=config)

    @classmethod
    def from_env(cls) -> Self:
        config = PostgreConfig.from_env()
        return cls(config)

    def create_exercise(
        self, exercise_uuid: str, exercise_title: str, exercise_text: str
    ) -> int:
        with self.repo._conn() as conn:
            insert_query = f"""
                INSERT INTO {self.repo._EXERCISE_TABLE} (uuid, title, text)
                VALUES (%s,%s,%s)
                RETURNING id
            """
            conn.execute(
                insert_query,
                (exercise_uuid, exercise_title, exercise_text),
            )

            exercise_id = conn.fetchone()[0]

            return exercise_id

    def update_exercise(self, exercise_uuid: str, exercise_text: str) -> None:
        with self.repo._conn() as conn:
            conn.execute(
                f"""UPDATE {self.repo._EXERCISE_TABLE} SET text=%s, where uuid=%s""",
                (
                    exercise_text,
                    exercise_uuid,
                ),
            )
            conn.fetchone()

            return

    def assign_exercise(self, candidate_uuid: str, exercise_uuid: str) -> bool:
        with self.repo._conn() as conn:
            try:
                conn.execute(
                    f"""INSERT INTO {self.repo._ASSIGMENTS_TABLE}
                        (candidate_uuid,exercise_uuid) VALUES (%s, %s)""",
                    (candidate_uuid, exercise_uuid),
                )
            except ForeignKeyViolation:
                return False

            return True

    def get_assigment_exercises(self, candidate_id: int) -> AssigmentExercises:
        with self.repo._conn() as conn:
            conn.execute(
                f"""
                SELECT c.name, c.email, c.uuid as c_uuid, e.uuid as e_uuid, e.title, e.text
                FROM {self.repo._CANDIDATES_TABLE} c
                JOIN {self.repo._ASSIGMENTS_TABLE} a ON a.candidate_uuid = c.uuid
                JOIN {self.repo._EXERCISE_TABLE} e ON e.uuid = a.exercise_uuid
                WHERE c.id = %s
                """,
                (candidate_id,),
            )
            rows = conn.fetchall()
            # TODO: Fix me at with indexes, index out if range rows[0][0]
            print(rows)
            candidate = Candidate(name=rows[0][0], email=rows[0][1], uuid=rows[0][2])
            exercises = [
                AssigmentExercise(
                    exercise_uuid=row[3],
                    exercise_title=row[4],
                    exercise_text=row[5],
                )
                for row in rows
            ]

            return AssigmentExercises(candidate=candidate, exercises=exercises)

    def get_exercises(self) -> Exercises:
        with self.repo._conn() as conn:
            conn.execute(
                f"""SELECT uuid, title, text from {self.repo._EXERCISE_TABLE}""",
            )
            exercises = conn.fetchall()

            return Exercises(
                exercises=[
                    Exercise(uuid=exercise[0], title=exercise[1], text=exercise[2])
                    for exercise in exercises
                ]
            )
