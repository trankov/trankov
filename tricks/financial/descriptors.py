from customtypes import CastDecimal
import validators


class DecimalAmount:
    """
    Descriptor for financial property values.
    Compulsory cast property value to Decimal if possible.
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.hidden_name = f"_{name}"

    def __get__(self, instance, owner):
        return instance.__dict__.setdefault(self.hidden_name, CastDecimal(".0"))

    def __set__(self, instance, value):
        instance.__dict__[self.hidden_name] = CastDecimal(str(value))

    def __delete__(self, instance):
        del instance.__dict__[self.hidden_name]


class ValidCurrency:
    """
    Descriptor for valid currency values.
    Check is 3-letters value consistent with ISO 4217:2015.
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.hidden_name = f"_{name}"

    def __get__(self, instance, owner):
        return instance.__dict__.setdefault(self.hidden_name, "RUB")

    def __set__(self, instance, value):
        validators.currency_match_iso4217(value)
        instance.__dict__[self.hidden_name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.hidden_name]
