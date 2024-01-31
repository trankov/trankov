"""
Tool to avoid many checks is each node of the attribute chain or in nested dict
is None.

>>> def user_info(request):
>>>     return {
>>>         "name": request.user.username,
>>>         "email": request.user.email,
>>>         "phone": GetAttr(request.user).from_str("contacts.phone_number") or "Undefined",
>>>         "gender": GetAttr(request.user).from_args("profile", "gender") or "🏳️‍🌈",
>>>         "address": GetAttr(request.user.json_data).from_keys("info", "geo", "address")
>>>     }

For awaitables:

>>> phone = await GetAttrAsync.from_str(request.user, "contacts.phone_number")
"""

from typing import Any, Mapping


class GetAttr:

    def __init__(self, obj: object):
        self.obj = obj

    def from_str(self, attr_string: str) -> Any | None:
        chain = attr_string.split(".")
        return self._iter_args(chain) if chain else None

    def from_args(self, obj: object, first_prop: str, *other_props) -> Any | None:
        props = (first_prop, *other_props)
        return self._iter_args(props)

    def _iter_args(self, arg_sequence):
        result = self.obj
        for arg in arg_sequence:
            result = getattr(result, arg, None)
            if result is None:
                return None
        return result

    def from_keys(self, **keys) -> Any | None:
        if not isinstance(self.obj, Mapping) or not keys:
            return None
        dictionary: Mapping = self.obj
        for key in keys:
            dictionary = dictionary.get(key, None)
            if not isinstance(dictionary, Mapping):
                return dictionary
        return dictionary


class GetAttrAsync:

    @classmethod
    async def from_str(cls, obj: object, attr_string: str) -> Any | None:
        _self = cls()
        await _self._init(obj)
        return _self._getattr.from_str(attr_string)

    @classmethod
    async def from_args(cls, obj: object, first_prop: str, *other_props) -> Any | None:
        _self = cls()
        await _self._init(obj)
        return _self._getattr.from_args(obj, first_prop, *other_props)

    @classmethod
    async def from_keys(cls, obj: object, **keys) -> Any | None:
        _self = cls()
        await _self._init(obj)
        return _self._getattr.from_keys(**keys)

    async def _init(self, obj):
        self._getattr = GetAttr(obj)
