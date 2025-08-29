from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Exercise:
    id: int
    title: str
    text: str
    author_id: int
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime]
