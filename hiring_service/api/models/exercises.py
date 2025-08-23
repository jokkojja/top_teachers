from pydantic import BaseModel


class Exercise(BaseModel):
    uuid: str
    title: str
    text: str


class Exercises(BaseModel):
    exercises: list[Exercise]
