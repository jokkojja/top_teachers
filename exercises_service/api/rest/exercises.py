from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from api.models.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from api.rest.dependencies import get_database_session
from app_globals import DatabaseSession


exercise_router = APIRouter(prefix="/api/v1/exercise")


@exercise_router.get("/{exercise_id}")
def get_exercise(
    exercise_id: int,
    database_session: DatabaseSession = Depends(get_database_session),
) -> ExerciseResponse:
    exercise = database_session.postgres.get_exercise(exercise_id)
    if exercise is None:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return ExerciseResponse(
        exercise_id=exercise.exercise_id,
        title=exercise.title,
        text=exercise.text,
        author_id=exercise.author_id,
        uuid=exercise.uuid,
        created_at=exercise.created_at,
        updated_at=exercise.updated_at,
    )


@exercise_router.put("/")
def create_exercise(
    exercise: ExerciseCreate,
    database_session: DatabaseSession = Depends(get_database_session),
) -> JSONResponse:
    exercise_id = database_session.postgres.create_exercise(
        title=exercise.title, text=exercise.text, author_id=exercise.author_id
    )
    if exercise_id is None:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Author with provided ID does not exist",
        )

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content=f"""Exercise was created with id {exercise_id}""",
    )


@exercise_router.patch("/{exercise_id}")
def update_exercise(
    exercise_id: int,
    exercise: ExerciseUpdate,
    database_session: DatabaseSession = Depends(get_database_session),
) -> JSONResponse:
    is_updated = database_session.postgres.update_exercise(
        exercise_id=exercise_id, text=exercise.text, updated_at=exercise.updated_at
    )
    print(exercise)
    if not is_updated:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Exercise with provided ID does not exist",
        )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=f"""Exercise with id {exercise_id} was updated""",
    )
