from datetime import datetime, UTC
import enum
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from loguru import logger

from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.models.candidate import CandidateResponse, CandidateCreate, Candidates
from api.rest.dependencies import get_database_controllers, get_kafka_producer
from app_globals import PostgreControllers
from kafka.producer import KafkaProducerService

candidate_router = APIRouter(prefix="/api/v1/candidate")


@enum.unique
class EventType(enum.StrEnum):
    CANDIDATE_CREATED = "CandidateCreated"


async def publish_candidate(
    candidate_uuid: str,
    producer: KafkaProducerService,
    event_type: EventType,
):
    topic = "data_replication.candidates"
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(UTC).isoformat(),
        "payload": {
            "candidate_uuid": candidate_uuid,
        },
    }
    await producer.send(topic, event)

    logger.info(f"Send event {event} to kafka topic {topic}")


@candidate_router.get("/")
def get_candidates(
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> Candidates:
    candidates = database_controllers.candidate_controller.get_candidates()
    if len(candidates.candidates) == 0:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Candidates(
        users=[
            CandidateResponse(name=candidate.name, email=candidate.email)
            for candidate in candidates
        ]
    )


@candidate_router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> CandidateResponse:
    candidate = database_controllers.candidate_controller.get_candidate(candidate_id)
    if candidate is None:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return CandidateResponse(name=candidate.name, email=candidate.email)


@candidate_router.put("/")
async def create_candidate(
    candidate: CandidateCreate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
    producer: KafkaProducerService = Depends(get_kafka_producer),
) -> JSONResponse:
    candidate_uuid = database_controllers.candidate_controller.create_candidate(
        candidate.name, candidate.email
    )
    if candidate_uuid is None:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content="Can't create candidate, something went wrong",
        )

    await publish_candidate(candidate_uuid, producer, EventType.CANDIDATE_CREATED)

    return JSONResponse(status_code=HTTP_200_OK, content="Candidate was created")
