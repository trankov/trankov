# The core concept of this approach is how to write a bit more transparent and a bit short code.
# This single case is about None as a default value in method/function argument.
# Obviously often we can set default in positional. In example below it could be such a:
# 
#     def setprop(self, prop_passed=self.prop): ...
# 
# But sometimes we need much flexible behaviour. 
# Imagine, in our example N().prop has been setted to None in some reason.
# Or, maybe, default value depends of variable type. For numbers it should be 0 but for strings - ''
# 
# So, instead of stairway of code, we can use the following syntax.
# It costs us just one lambda definition and one checking string.
# As a result, we prevent appearing of None in our logic and still fluent operating with defaults.
# And it's short and well readable.


_None = lambda value, default_value: value or default_value

class N:
    prop = 22
    def setprop(self, prop_passed=None):
        self.prop = _None(prop_passed, self.prop or 0)
