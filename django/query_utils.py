"""
Using dynamic sets of Q objects in Django queries it is no obvious
how to combine them with something except AND method (which is default).

This module provides `GatherQ` class which can be used to combine Q objects
in one line using the |, & or ^ operators between dynamic Q-sequence and
class instance at right side.

For example we got some seek parameters from web API and we want to
combine them in Q object using OR.

>>> lookup = (Q(key=value) for key, value in params.items()) | GatherQ()

Then we can use `lookup` to filter our queryset:
>>> MyModel.objects.filter(lookup)

Combine using XOR:
>>> (Q(key=value) for key, value in params.items()) ^ GatherQ()

Combine using AND (actually not necessary, because it is default):
>>> (Q(key=value) for key, value in params.items()) & GatherQ()
"""

from functools import reduce
from operator import and_, or_, xor
from typing import Callable, Iterable

from django.db.models import Q


class GatherQ:
    """
    Helper class for combining Q objects. If you have a bunch of Q objects,
    use this class to combine them using the |, & or ^ operators in one line.

    >>> (Q(pk=1), Q(pk=2), Q(pk=3)) | GatherQ()
    >>> <Q: (OR: ('pk', 1), ('pk', 2), ('pk', 3))>
    """
    def __rand__(self, other: Iterable[Q]) -> Q:
        """
        Combine Q objects using AND.
        """
        return self._gather(other, and_)

    def __ror__(self, other: Iterable[Q]) -> Q:
        """
        Combine Q objects using OR.
        """
        return self._gather(other, or_)

    def __rxor__(self, other: Iterable[Q]) -> Q:
        """
        Combine Q objects using XOR.
        """
        return self._gather(other, xor)

    def _gather(self, other: Iterable[Q], op: Callable) -> Q:
        """
        Combine Q objects using the operator given.
        """
        return reduce(op, other)
