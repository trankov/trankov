from collections.abc import Mapping, MutableSequence, Sequence
from typing import Any


NonStrSequence = MutableSequence | tuple


class TypeContainer:
    """Base class for type-marked arguments"""

    def __init__(self, _v):
        self._v = _v

    def __call__(self, target):
        return self._v

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._v!r})'


class Attr(TypeContainer):
    """
    Extract value as an object attribute

    >>> import sys
    >>> base_prefix = Attr('base_prefix')
    >>> base_prefix(sys)
    '/opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12'

    Any valid attribute name can be used as an argument:

    >>> import platform
    >>> system_attr = Attr('system')
    >>> system = system_attr(platform)
    >>> system()
    'Darwin'
    """

    def __call__(self, target) -> Any | None:
        return getattr(target, self._v, None)


class Key(TypeContainer):
    """
    Extract value as a key mapped item

    >>> one_in = Key('one')
    >>> mapping = {'one': 1, 'two': 2, 'three': 3, 'anyhow': 4}
    >>> one_in(mapping) == 1
    True

    Any valid key can be used as an argument:

    >>> none_in = Key(None)
    >>> mapping = {'one': 1, 'two': 2, True: 3, None: 4, dict: 12}
    >>> none_in(mapping)
    4
    >>> Key(dict)(mapping) == 12
    True
    """

    def __call__(self, target) -> Any | None:
        return target.get(self._v) if isinstance(target, Mapping) else None


class Index(TypeContainer):
    """
    Extract value as an integer index from sequences (but not from strings)

    >>> first_item_of = Index(0)
    >>> sequence = ['one', 'two', 'three', 'anyhow']
    >>> first_item_of(sequence) == 'one'
    True

    Any valid index can be used as an argument:

    >>> last_item_of = Index(-1)
    >>> sequence = ['one', 'two', 'three', 'anyhow']
    >>> last_item_of(sequence)
    'anyhow'
    >>> Index(-2)(sequence)
    'three'
    """

    def __call__(self, target) -> Any | None:
        return target[int(self._v)] if isinstance(target, NonStrSequence) else None
