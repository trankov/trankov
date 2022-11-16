from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class ISO3166Item(BaseModel):
    Code: int
    Short: str
    Full: Optional[str] = Field(...)
    A2: str = Field(min_length=2, max_length=2)
    A3: str = Field(min_length=3, max_length=3)


class ISO3166List(BaseModel):
    items: List[ISO3166Item]


class ISO_3166:
    def __init__(self, filename: Optional[str] = None) -> None:
        filename = filename or "OK_MK_ISO3166_004-97_025-2001(072021).json"
        self.list = ISO3166List.parse_file(Path(__file__).parent / filename)

    @property
    def A2_codes(self) -> List[str]:
        if self.list is None:
            return []
        return sorted(filter(None, {item.A2 for item in self.list.items}))

    @property
    def A3_codes(self) -> List[str]:
        if self.list is None:
            return []
        return sorted(filter(None, {item.A3 for item in self.list.items}))

    @property
    def num_codes(self) -> List[int]:
        if self.list is None:
            return []
        return sorted(filter(None, {item.Code for item in self.list.items}))
