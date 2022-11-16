from string import hexdigits

from .iso3166 import ISO_3166  # country codes
from .iso4217 import ISO4217_2015  # currency codes


def currency_match_iso4217(value):
    if value not in ISO4217_2015().char_codes:
        raise ValueError(f"There is no `{value}` in ISO-2417:2015")
    return value


def inn_conditions(value: str):
    if value is None:
        return None
    val_len = len(value)
    if all((value.isdecimal, any((val_len == 10, val_len == 12)))):
        return value
    raise ValueError("INN must be 10 or 12 digits")


def phone_is_e164(value):
    if value is None:
        return None
    if all((value.isdecimal, 3 < len(value) < 15)):
        return value
    raise ValueError(f"Phone {value} incorrect (3 to 15 digits of ITU-T E.164)")


def phone_or_email(values):
    if {values.get("phone"), values.get("email")} == {None}:
        raise ValueError("There must be at least one of <phone> or <email>")
    return values


def quantity_is_numeric(value):
    if value.isdigit():
        return value
    raise ValueError(f"Value {value} must be string of integers")


def is_prod_code_hex_max32(value):
    # Example of product code (from docs):
    # 00 00 00 01 00 21 FA 41 00 23 05 41 00 00 00 00
    # 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00
    hex_seq = value.upper().split(" ")
    if all(
        (
            1 <= len(hex_seq) <= 32,
            all(
                (all(hexdigit in hexdigits for hexdigit in chunk), len(chunk) == 2)
                for chunk in hex_seq
            ),
        )
    ):
        return value
    raise ValueError(f"`product_code` {value} is invalid")


def country_code_len2(value):
    if value in ISO_3166().A2_codes:
        return value
    raise ValueError(f'Bad Alfa-2 country code: "{value}"')


class MetadataValidator(dict):
    def full_validation(self):
        self.max16keys()
        self.key32chars()
        self.value512UTF8chars()

    def max16keys(self):
        if len(self) > 16:
            raise KeyError("Too many keys (max=16)")

    def key32chars(self):
        for k in self.keys():
            if len(k) > 32:
                raise KeyError(f'Too long key "{k}" (max=32)')

    def value512UTF8chars(self):
        for v in self.values():
            if type(v) is not str:
                raise ValueError("All values must be UTF-8 strings")
            if len(v) > 512:
                raise ValueError(f'Too long value "{v[:8]}…{v[-8:]}" (max=512)')
