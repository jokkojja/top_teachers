from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class AppGlobals:
    @classmethod
    async def create() -> Self:
        pass
