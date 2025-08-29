from fastapi import APIRouter, Depends
from fastapi.responses import Response

from starlette.status import (
    HTTP_204_NO_CONTENT,
)

from api.models.exercises import Exercises, Exercise
from api.rest.dependencies import get_database_controllers
from app_globals import PostgreControllers

exercises_router = APIRouter(prefix="/api/v1/exercise")


@exercises_router.get("/")
def get_exercises(
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> Exercises:
    exercises = database_controllers.exercise_controller.get_exercises()
    if exercises is None:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Exercises(
        exercises=[
            Exercise(uuid=exercise.uuid, title=exercise.title, text=exercise.text)
            for exercise in exercises
        ]
    )
