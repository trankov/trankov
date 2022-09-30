"""
    Dynamic `upload_to` path for `FileField` or `ImageField`.
    Does not produce redundant migrations (due to __eq__ and @deconstructible).
    Methods can provide any logic you need via "self" variables.
    As they are Callables, you can assign them to upload_to parameter,
    just make them pass (instance, filename) as it demands.
    __init__ get any necessary parameters reacheble from methods.

    >>> class UserProfile(models.Model):
    >>>     image = models.ImageField(
    >>>         verbose_name="Profile Image",
    >>>         upload_to=UploadTo("profile_folder").my_method,
    >>>     )

"""

from pathlib import Path
from typing import Callable

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    def __init__(self, any_args):
        self.any_args = any_args

    def __eq__(self, other):
        return self.any_args == other.any_args

    def any_method(self, instance, filename) -> Path:
        return (
            Path(instance.__class__.__name__) / str(self.any_args) / filename
        )

    def any_other_method(self, instance, filename) -> Path:
        return Path()

    def from_iterable(self, instance, filename):
        try:
            iter(self.any_args)
        except TypeError as type_error:
            raise TypeError from type_error
        return Path(*map(str, self.any_args)) / filename
