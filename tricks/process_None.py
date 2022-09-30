_None = lambda value, default_value: value or default_value


class N:
    prop = 22

    def setprop(self, prop_passed=None):
        self.prop = _None(prop_passed, self.prop or 0)


# An another approach is better in readability and shorter, but declaration
# is complex an using is non-intuitive. But it is convenient when there are
# a lot of checks and they are of different severity. Following example
# demonstrates check both for None and False value.


class Avoid:
    def __init__(self, value):
        self.value = value

    def __floordiv__(self, default_value):
        """Returns default if None"""
        return default_value if self.value is None else self.value

    def __truediv__(self, default_value):
        """Returns default if False"""
        return self.value if bool(self.value) else default_value

    def __call__(self, default_value):
        """Returns default if not exist"""
        if self.value in locals():
            return locals()[self.value]
        return globals().get(self.value, default_value)


value = 0
default_value = 2
print(Avoid(value) // default_value)
print(Avoid(value) / default_value)

print(Avoid("value")(default_value))
print(Avoid("value_")(default_value))


# So, it could be written as:
#
#     value = Avoid(value) / default_value
#
# Why not to Avoid(value, default_value)? First, operator defines severity.
# We can define another if we need (f.e. for checking is numeric value positive
# or whatever). Second, here we don't need to remember which argument means what.
