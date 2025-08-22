from pydantic import BaseModel


class CandidateResponse(BaseModel):
    uuid: str
    name: str


class Candidates(BaseModel):
    users: list[CandidateResponse]
