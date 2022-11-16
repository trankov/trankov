from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from pydantic import BaseModel


# Currencies list


class ISO4217_2015Item(BaseModel):
    Entity: str
    Currency: str
    AlphabeticCode: Optional[str]
    NumericCode: Optional[int]
    MinorUnit: Optional[int]
    Fund: Optional[bool]

    class Config:
        allow_mutation = False


class ISO4217_2015List(BaseModel):
    items: List[ISO4217_2015Item]

    class Config:
        allow_mutation = False


class ISO4217_2015:
    def __init__(self, filename: Optional[str] = None) -> None:
        filename = filename or "ISO-4217_2015.json"
        self.list = ISO4217_2015List.parse_file(Path(__file__).parent / filename)

    def _find(self, field: str, value: Union[str, bool, int]) -> list:
        if self.list is None:
            return []
        return [item for item in self.list.items if getattr(item, field) == value]

    def entity(self, value: str) -> list:
        return self._find("Entity", value)

    def currency(self, value: str) -> list:
        return self._find("Currency", value)

    def code_char(self, value: str) -> list:
        return self._find("AlphabeticCode", value)

    def alphabetic_code(self, value: str) -> list:  # ALIAS METHOD
        return self.code_char(value)

    def code_num(self, value: int) -> list:
        return self._find("NumericCode", value)

    def numeric_code(self, value: int) -> list:  # ALIAS METHOD
        return self.code_num(value)

    def minor_unit(self, value: int) -> list:
        return self._find("MinorUnit", value)

    def minor(self, value: int) -> list:  # ALIAS METHOD
        return self.minor_unit(value)

    def is_fund(self, value: bool) -> list:
        return self._find("Fund", value)

    @property
    def char_codes(self) -> List[str]:
        if self.list is None:
            return []
        return sorted(
            {item.AlphabeticCode for item in self.list.items if item.AlphabeticCode}
        )

    @property
    def num_codes(self) -> List[int]:
        if self.list is None:
            return []
        return sorted(
            {item.NumericCode for item in self.list.items if item.NumericCode}
        )

    @property
    def code_pairs(self) -> List[Tuple[str, int] | Tuple[Any, ...]]:
        if self.list is None:
            return []
        return sorted(
            {
                (item.AlphabeticCode, item.NumericCode)
                for item in self.list.items
                if (item.AlphabeticCode and item.NumericCode)
            }
        )
