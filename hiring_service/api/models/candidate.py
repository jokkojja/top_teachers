from pydantic import BaseModel


class CandidateResponse(BaseModel):
    name: str
    email: str


class Candidates(BaseModel):
    users: list[CandidateResponse]


class CandidateCreate(BaseModel):
    name: str
    email: str
