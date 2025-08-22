from fastapi import APIRouter, Depends
from fastapi.responses import Response

from starlette.status import (
    HTTP_204_NO_CONTENT,
)

from api.models.candidate import (
    CandidateResponse,
    Candidates,
)
from api.rest.dependencies import get_database_controllers
from app_globals import PostgreControllers

candidate_router = APIRouter(prefix="/api/v1/candidate")


@candidate_router.get("/")
def get_candidates(
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> Candidates:
    candidates = database_controllers.candidate_controller.get_candidates()
    if len(candidates.candidates) == 0:
        return Response(status_code=HTTP_204_NO_CONTENT)

    return Candidates(
        users=[
            CandidateResponse(uuid=candidate.uuid, name=candidate.name)
            for candidate in candidates
        ]
    )
