"""
ManagerPlus:

    Don't raising error on MyModel.DoesNotExists exception and returns None
    >>> MyModel.objects.get_or_none(pk=100)


    Aviods DoesNotExists or MultipleObjectsReturned exceptions,
    returns first/last object or None
    >>> MyModel.objects.none_or_first(username="Tahiro")
    >>> MyModel.objects.none_or_last(username="Motoyuki")


    Checks is at least one object exists, then returns True or False
    >>> MyModel.objects.has_any(model="Ford", age__gte=5)


ModelPlus:
    - Including ManagerPlus by default
    - Has method to_dict() which returns object as a dictionary


ModelStat:
    - Including created_at and updated_at by default


Example:

    >>> from enhanced_models import ModelPlus, ModelStat

    >>> class MyModel(ModelPlus, ModelStat):
    >>>     ...

    >>> if my_obj := MyModel.objects.last_or_none(tracking_number="23456"):
    >>>     return json_dumps(my_obj.to_dict())

"""

import os

from itertools import chain
from typing import Any, Sequence

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from django.db import connection, models


def get_env_username():
    "Returns username connected to DB server in OS environment"
    return os.getlogin()


def get_db_username():
    "Returns username for connection session in DB server environment"
    return connection._connections.settings[connection._alias]["USER"]


class ManagerPlus(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def has_any(self, **kwargs) -> bool:
        """
        `True` if `self.filter(**kwargs)` is not empty, else `False`
        """
        return bool(self.filter(**kwargs).all)

    def none_or_first(self, **kwargs):
        try:
            return self.get(**kwargs)
        except MultipleObjectsReturned:
            return self.filter(**kwargs).first()
        except ObjectDoesNotExist:
            return None

    def none_or_last(self, **kwargs):
        try:
            return self.get(**kwargs)
        except MultipleObjectsReturned:
            return self.filter(**kwargs).last()
        except ObjectDoesNotExist:
            return None

    def random(self):
        return self.order_by("?").first()


class ModelPlus(models.Model):

    objects = ManagerPlus()

    @property
    def _allfields(self):
        """Iterable with all fields in the model"""
        return chain(
                getattr(self._meta, "concrete_fields", []),
                self._meta.private_fields,
            )

    def to_dict(self, fields: Sequence | None = None) -> dict[str, Any]:
        """
        Returns model object as a dictionary. If `fields` is specified,
        returns a precised fields only.

        Unexistent fields are ignored with no exception raise.
        """
        return {
            field.name: field.value_from_object(self)
            for field in self._allfields if fields is None or field in fields
        }

    def update_fields(self, skip_extra: bool = True, **kwargs):
        """
        Updates and saves instance according to `kwargs`.

        If `skip_extra` is `True`, fields not in model are skpipped,
        otherwise AttributeError will raise.
        """
        fieldnames = {i.name for i in self._allfields}
        kwnames = set(kwargs.keys())
        if not kwnames.issubset(fieldnames) and not skip_extra:
            raise AttributeError(
                f'Wrong field(s) {", ".join(kwnames.difference(fieldnames))}'
            )
        fields2update = ()
        for k, v in kwargs.items():
            if k in fieldnames:
                setattr(self, k, v)
                fields2update += (k,)
        self.save(update_fields=fields2update)
        return self

    class Meta:
        abstract = True


class ModelStat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_env_uname = models.CharField(
        verbose_name="OS User",
        max_length=32,
        default=get_env_username,
    )
    created_db_uname = models.CharField(
        verbose_name="DB User",
        max_length=32,
        default=get_db_username,
    )

    class Meta:
        abstract = True
