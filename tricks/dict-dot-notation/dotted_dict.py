"""
The main reason why Python's dict doesn't support dot notation is because
class attribute name is always string, not hashable object.

So, this implementation provides a limited usage of dict, guess all keys must
be strings only.

    >>> d = {"a": 1, "b": 2}
    >>> dot_dict = DotDict({"c": 3, "d": 4, "e": d})

    >>> dot_dict.c      # 3
    >>> dot_dict.e      # {'a': 1, 'b': 2}
    >>> dot_dict.e.a    # 1

"""


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(key, str):
                raise TypeError(f"Attributes must be strings, not {type(key)} as {key}")
            if isinstance(value, dict):
                self[key] = DotDict(value)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
