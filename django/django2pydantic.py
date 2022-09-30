import datetime
from decimal import Decimal
from pydantic import IPvAnyAddress
from uuid import UUID
from typing import Any
from django.db.models import Field


__all__ = [
    "TYPES",
    "type_field",
    "match_type",
    "extract_type",
]

TYPES = {
    "AutoField": int,
    "BigAutoField": int,
    "BigIntegerField": int,
    "BinaryField": bytes,
    "BooleanField": bool,
    "CharField": str,
    "DateField": datetime.date,
    "DateTimeField": datetime.datetime,
    "DecimalField": Decimal,
    "DurationField": datetime.timedelta,
    "EmailField": str,
    "FileField": str,
    "FilePathField": str,
    "FloatField": float,
    "GenericIPAddressField": IPvAnyAddress,
    "IntegerField": int,
    "IPAddressField": IPvAnyAddress,
    "JSONField": Any,
    "NullBooleanField": bool,
    "PositiveBigIntegerField": int,
    "PositiveIntegerField": int,
    "PositiveSmallIntegerField": int,
    "SlugField": str,
    "SmallIntegerField": int,
    "TextField": str,
    "TimeField": datetime.time,
    "UUIDField": UUID,
}


def type_field(field: Field) -> str:
    return field.deconstruct()[1].split(".")[-1]


def match_type(type_: str) -> type:
    return TYPES.get(type_, int)


def extract_type(field: Field) -> type:
    return match_type(type_field(field))
