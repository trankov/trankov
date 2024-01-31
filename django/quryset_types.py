"""
Types for django.db.models.QuerySet in `isinstance()` check.

>>> queryset = MyModel.objects.all()

>>> if isinstance(queryset, SingleItemQueryset):
>>>     return queryset.first()
>>> elif isinstance(queryset, MultiItemQueryset):
>>>     return some_function(queryset)
>>> elif isinstance(queryset, EmptyQueryset):
>>>     return None

>>> # Another example

>>> result = (
>>>     some_function(queryset)
>>>     if isinstance(queryset, NonEmptyQueryset)
>>>     else None
>>> )
"""

from django.db import models


class _SingleItemQueryset(type):
    def __instancecheck__(self, arg) -> bool:
        try:
            return bool(arg) and isinstance(arg, models.QuerySet) and len(arg) == 1
        except TypeError:
            return False


class _MultiItemQueryset(type):
    def __instancecheck__(self, arg) -> bool:
        try:
            return bool(arg) and isinstance(arg, models.QuerySet) and len(arg) > 1
        except TypeError:
            return False


class _EmptyQueryset(type):
    def __instancecheck__(self, arg) -> bool:
        try:
            return isinstance(arg, models.QuerySet) and not bool(arg)
        except TypeError:
            return False


class _NonEmptyQueryset(type):
    def __instancecheck__(self, arg) -> bool:
        try:
            return isinstance(arg, models.QuerySet) and bool(arg)
        except TypeError:
            return False


class EmptyQueryset(metaclass=_EmptyQueryset):
    """
    Returns `True` on `isinstance()` check when
    `django.db.models.QuerySet([])`. If `QuerySet` is not empty,
    or it is not a `QuerySet`, returns `False`.
    """

    pass


class MultiItemQueryset(metaclass=_MultiItemQueryset):
    """
    Returns `True` on `isinstance()` check when
    `django.db.models.QuerySet([Model, ...])`. If `QuerySet` is empty,
    or contains only one `Model`s or it is not a `QuerySet`,
    returns `False`.
    """

    pass


class SingleItemQueryset(metaclass=_SingleItemQueryset):
    """
    Returns `True` on `isinstance()` check when
    `django.db.models.QuerySet([Model])`. If `QuerySet` does not contain
    only one `Model`, or it is not a `QuerySet`, returns `False`.
    """

    pass


class NonEmptyQueryset(metaclass=_NonEmptyQueryset):
    """
    Returns `True` on `isinstance()` check when
    `django.db.models.QuerySet` is not empty. If `QuerySet`
    is empty, or is not a `QuerySet`, returns `False`.
    """

    pass
