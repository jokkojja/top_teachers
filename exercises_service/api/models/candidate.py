from pydantic import BaseModel


class CandidateResponse(BaseModel):
    id: int
    uuid: str
    name: str


class Candidates(BaseModel):
    users: list[CandidateResponse]
