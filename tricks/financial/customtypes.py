from decimal import Decimal


class CastDecimal(Decimal):
    """
    Cast any possible type of given number to a Decimal type.
    Provides arithmetic and logical operators for it, converting operands
    to CastDecimal and returns Decimal or bool.
    """

    def __init__(self, *args, **kwargs):
        self.__value = self.__cast(args[0])
        super().__init__(*args[1:], **kwargs)

    def __add__(self, other):
        __result = self.__value + self.__cast(other)
        return CastDecimal(__result)

    def __sub__(self, other):
        __result = self.__value - self.__cast(other)
        return CastDecimal(__result)

    def __rsub__(self, other):
        __result = self.__cast(other) - self.__value
        return CastDecimal(__result)

    def __mul__(self, other):
        __result = self.__value * self.__cast(other)
        return CastDecimal(__result)

    def __truediv__(self, other):
        __result = self.__value / self.__cast(other)
        return CastDecimal(__result)

    def __rtruediv__(self, other):
        __result = self.__cast(other) / self.__value
        return CastDecimal(__result)

    def __floordiv__(self, other):
        __result = self.__value // self.__cast(other)
        return CastDecimal(__result)

    def __rfloordiv__(self, other):
        __result = self.__cast(other) // self.__value
        return CastDecimal(__result)

    def __mod__(self, other):
        __result = self.__value % self.__cast(other)
        return CastDecimal(__result)

    def __rmod__(self, other):
        # Will not work with "0.1" % CastDecimal and other strings at left,
        # because str's "%" means string format operator
        __result = self.__cast(other) % self.__value
        return CastDecimal(__result)

    def __divmod__(self, other):
        return divmod(self.__value, self.__cast(other))

    def __rdivmod__(self, other):
        return divmod(self.__cast(other), self.__value)

    __iadd__ = __radd__ = __add__
    __isub__ = __sub__
    __imul__ = __rmul__ = __mul__
    __itruediv__ = __truediv__
    __ifloordiv__ = __floordiv__
    __imod__ = __mod__

    def __eq__(self, other):
        return self.__value == self.__cast(other)

    def __lt__(self, other):
        return self.__value < self.__cast(other)

    def __le__(self, other):
        return self.__value <= self.__cast(other)

    def __ne__(self, other):
        return self.__value != self.__cast(other)

    def __gt__(self, other):
        return self.__value > self.__cast(other)

    def __ge__(self, other):
        return self.__value >= self.__cast(other)

    def __cast(self, value):
        if isinstance(value, Decimal):
            return value
        if isinstance(value, (int, float)):
            return Decimal(str(value))
        if isinstance(value, str):
            value = value.replace(",", ".")
            if not value.replace(".", "", 1).isdigit():
                raise ValueError(f"Cannot convert {value!r} to valid number")
            return Decimal(value)
        raise TypeError(f"{type(value)!r} is not a valid type for amount")
