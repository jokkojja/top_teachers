from pydantic import BaseModel


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    uuid: str


class Candidates(BaseModel):
    users: list[CandidateResponse]


class CandidateCreate(BaseModel):
    name: str
    email: str


class AssigmentExercise(BaseModel):
    exercise_uuid: str
    exercise_title: str
    exercise_text: str


class AssigmentExercises(BaseModel):
    candidate: CandidateResponse
    exercises: list[AssigmentExercise]
