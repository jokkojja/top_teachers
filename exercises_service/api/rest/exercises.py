from datetime import datetime, UTC
import enum
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from loguru import logger
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from api.models.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from api.rest.dependencies import get_database_controllers, get_kafka_producer
from app_globals import PostgreControllers
from kafka.producer import KafkaProducerService

exercise_router = APIRouter(prefix="/api/v1/exercise")


@enum.unique
class EventType(enum.StrEnum):
    EXERCISE_CREATED = "ExerciseCreated"
    EXERCISE_UPDATED = "ExerciseUpdated"


async def publish_exercise(
    exercise_uuid: str,
    producer: KafkaProducerService,
    event_type: EventType,
):
    topic = "data_replication.exercises"
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(UTC).isoformat(),
        "payload": {
            "exercise_uuid": exercise_uuid,
        },
    }
    await producer.send(topic, event)

    logger.info(f"Send event {event} to kafka topic {topic}")


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
async def create_exercise(
    exercise: ExerciseCreate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
    producer: KafkaProducerService = Depends(get_kafka_producer),
) -> JSONResponse:
    # Formal comm. Streaming exercise to hiring service. Topic: data_replication.exercises
    exercise_uuid = database_controllers.exercises_controller.create_exercise(
        title=exercise.title, text=exercise.text, author_id=exercise.author_id
    )
    if exercise_uuid is None:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Author with provided ID does not exist",
        )

    await publish_exercise(exercise_uuid, producer, EventType.EXERCISE_CREATED)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content="Exercise was created",
    )


@exercise_router.patch("/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    exercise: ExerciseUpdate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
    producer: KafkaProducerService = Depends(get_kafka_producer),
) -> JSONResponse:
    # Formal comm. Streaming exercise to hiring service. Topic: data_replication.exercises
    exercise_uuid = database_controllers.exercises_controller.update_exercise(
        exercise_id=exercise_id, text=exercise.text, updated_at=exercise.updated_at
    )
    if exercise_uuid is None:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Exercise with provided ID does not exist",
        )

    await publish_exercise(exercise_uuid, producer, EventType.EXERCISE_UPDATED)
    return JSONResponse(
        status_code=HTTP_200_OK,
        content=f"Exercise with id {exercise_id} was updated",
    )


@exercise_router.post("/")
def assign_exercise(
    candidate_id: int,
    exercise_id: int,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
):
    # Func comm. Buisisness event to hiring service. Topic: domain.homework
    is_assigned = database_controllers.exercises_controller.assign_exercise(
        candidate_id, exercise_id
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
