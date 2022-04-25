# Transform each list element according to operators (*, /, //, %, **) or apply callable when @
# Also inherits all methods and properties from type "list".

# n = extlist([1, 2, 3])
# n * 2 == [2, 4, 6]
# n ** 2 == [4, 16, 36]
# n @ str == ['1', '2', '3']

# n = extlist('abcde')
# n = ['a', 'b', 'c', 'd', 'e']
# n @ str.upper == ['A', 'B', 'C', 'D', 'E']

# Does not transform object itself. Just returns new list.
# Use n = n * 2 to replace original values.


class extlist(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
    def __mul__(self, __v):
        return [__i * __v for __i in self]
    def __truediv__(self, __v):
        return [__i / __v for __i in self]
    def __floordiv__(self, __v):
        return [__i // __v for __i in self]
    def __mod__(self, __v):
        return [__i % __v for __i in self]
    def __pow__(self, __v):
        return [__i ** __v for __i in self]
    def __matmul__(self, __v):
        if not callable(__v):
            raise TypeError('Operand must be callable')
        return [__v(__i) for __i in self]
