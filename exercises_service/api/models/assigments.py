from pydantic import BaseModel


class AssigmentCreate(BaseModel):
    candidate_uuid: str
    exercise_uuid: str


class Assigment(BaseModel):
    id: int
    candidate_uuid: str
    exercise_uuid: str


class Assigments(BaseModel):
    assigments: list[Assigment]
