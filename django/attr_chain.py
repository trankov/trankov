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

    def _iter_args(self, arg0):
        result = self.obj
        for chainlink in arg0:
            result = getattr(result, chainlink, None)
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
