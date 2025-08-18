from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response


from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from api.models.candidate import CandidateResponse, CandidateCreate, Candidates
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
def create_candidate(
    candidate: CandidateCreate,
    database_controllers: PostgreControllers = Depends(get_database_controllers),
) -> JSONResponse:
    candidate_id = database_controllers.candidate_controller.create_candidate(
        candidate.name, candidate.email
    )

    return JSONResponse(
        status_code=HTTP_200_OK, content=f"Candidate was created with id {candidate_id}"
    )
