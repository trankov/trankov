from collections.abc import Mapping, MutableSequence
from typing import Any

from .types import Attr, Index, Key, TypeContainer
from .utils import ArgsProcessor


NonStrSequence = MutableSequence | tuple


class PullOut:
    def __init__(self, *args) -> None:
        self.args = ArgsProcessor(*args).prepare()

    def From(self, object_from) -> Any:  # noqa: N802 (Ruff)
        self.obj = object_from
        return self._extract_args()

    def _extract_next(self, what_to_extract: Any, from_where: Any) -> Any:
        if isinstance(what_to_extract, TypeContainer):
            return what_to_extract(from_where)
        if isinstance(from_where, Mapping):
            return Key(what_to_extract)(from_where)
        if isinstance(from_where, NonStrSequence):
            return Index(what_to_extract)(from_where)
        return Attr(what_to_extract)(from_where)

    def _extract_args(self) -> Any | None:
        _obj = self.obj
        for arg in self.args:
            try:
                _obj = self._extract_next(arg, _obj)
            except (ValueError, TypeError, KeyError):
                return None
            if _obj is None:
                break
        return _obj
