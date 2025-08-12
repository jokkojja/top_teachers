from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Exercise(BaseModel):
    title: str
    text: str
    author_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]
    # for cross service
    uuid: str
