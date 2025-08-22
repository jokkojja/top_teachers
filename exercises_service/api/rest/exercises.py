from datetime import datetime, UTC
import enum
import uuid

from api.models.assigments import Assigment, AssigmentCreate, Assigments
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
    EXERCISE_ASSIGNED = "ExerciseAssigned"


async def publish_exercise(
    producer: KafkaProducerService,
    event_type: EventType,
    payload: dict[str, str],
):
    topic = "data_replication.exercises"
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(UTC).isoformat(),
        "payload": payload,
    }
    await producer.send(topic, event)

    logger.info(f"Send event {event} to kafka topic {topic}")


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

    payload = {
        "exercise_uuid": exercise_uuid,
        "exercise_title": exercise.title,
        "exercise_text": exercise.text,
    }
    await publish_exercise(
        producer=producer, event_type=EventType.EXERCISE_CREATED, payload=payload
    )

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content="Exercise was created",
    )


@exercise_router.get("/assigments")
def get_assigments(
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> Assigments:
    assigments = database_controllers.exercises_controller.get_assigments()
    if len(assigments.assigments) == 0:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Assigments(
        assigments=[
            Assigment(
                id=assigment.id,
                candidate_uuid=assigment.candidate_uuid,
                exercise_uuid=assigment.exercise_uuid,
            )
            for assigment in assigments
        ]
    )


@exercise_router.post("/assign")
async def assign_exercise(
    assigne_create: AssigmentCreate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
    producer: KafkaProducerService = Depends(get_kafka_producer),
) -> JSONResponse:
    # Func comm. Buisisness event to hiring service. Topic: domain.homework
    is_assigned = database_controllers.exercises_controller.assign_exercise(
        assigne_create.candidate_uuid, assigne_create.exercise_uuid
    )

    if not is_assigned:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content="Candidate or exercise with such UUID doesnt exist",
        )

    payload = {
        "exercise_uuid": assigne_create.exercise_uuid,
        "candidate_uuid": assigne_create.candidate_uuid,
    }

    await publish_exercise(
        producer=producer, event_type=EventType.EXERCISE_ASSIGNED, payload=payload
    )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=f"Exercise {assigne_create.exercise_uuid} were assigned to candidate {assigne_create.candidate_uuid}",
    )


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

    payload = {"exercise_uuid": exercise_uuid, "exercise_text": exercise.text}
    await publish_exercise(
        producer=producer, event_type=EventType.EXERCISE_UPDATED, payload=payload
    )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=f"Exercise with id {exercise_id} was updated",
    )
