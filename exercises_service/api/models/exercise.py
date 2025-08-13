from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExerciseCreate(BaseModel):
    title: str
    text: str
    author_id: int


class ExerciseResponse(BaseModel):
    exercise_id: int
    title: str
    text: str
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    uuid: str


class ExerciseUpdate(BaseModel):
    text: str
    updated_at: datetime = Field(default_factory=datetime.now)
