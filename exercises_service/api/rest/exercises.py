from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from uuid import UUID
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from api.models.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from api.rest.dependencies import get_database_controllers
from app_globals import PostgreControllers


exercise_router = APIRouter(prefix="/api/v1/exercise")


@exercise_router.get("/{exercise_id}")
def get_exercise(
    exercise_id: int,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> ExerciseResponse:
    exercise = database_controllers.exercises_controller.get_exercise(exercise_id)
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
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> JSONResponse:
    # Formal comm. Streaming exercise to hiring service
    exercise_id = database_controllers.exercises_controller.create_exercise(
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
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> JSONResponse:
    # Formal comm. Streaming exercise to hiring service
    is_updated = database_controllers.exercises_controller.update_exercise(
        exercise_id=exercise_id, text=exercise.text, updated_at=exercise.updated_at
    )
    if not is_updated:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Exercise with provided ID does not exist",
        )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=f"Exercise with id {exercise_id} was updated",
    )


@exercise_router.post("/")
def assign_exercise(
    candidate_uuid: UUID,
    exercise_uuid: UUID,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
):
    # Func comm. Buisisness event to hiring service
    is_assigned = database_controllers.exercises_controller.assign_exercise(
        candidate_uuid, exercise_uuid
    )

    if not is_assigned:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Candidate or exercise with such UUID doesnt exist",
        )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content="Exercise were assigned to candidate",
    )
