from collections.abc import Iterable
from typing import Any

from django.db.models import TextChoices


class _TextChoiceMeta(type):
    """Метакласс для проверки типов choices."""

    def __instancecheck__(cls, instance: Any) -> bool:
        return (
            isinstance(instance, TextChoices)
            and isinstance(type(instance), Iterable)
            and instance in type(instance)
        )


class TextChoiceType(metaclass=_TextChoiceMeta):
    """
    Базовый класс для проверки типов choices.

    >>> def method_getting_choices_item(precise_choice: models.TextChoices) -> None:
    >>>    if not isinstance(precise_choice, TextChoiceType):
    >>>        raise ValueError(f'Invalid choice value: {precise_choice}')
    >>>    # ... остальной код
    """
