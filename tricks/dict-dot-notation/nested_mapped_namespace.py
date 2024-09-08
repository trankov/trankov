from typing import Mapping, Sequence

# TODO Add support for Sequence values which maybe contains Mapping

class MappedNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return (
            f'{self.__class__.__name__}'
            f'({", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())})'
        )


def nested_mapped_namespace(dict_data: Mapping) -> MappedNamespace:
    assert isinstance(dict_data, Mapping), "Have to be a valid Mapping type"
    return MappedNamespace(
        **dict(
            (k, nested_mapped_namespace(v)) if isinstance(v, Mapping) else (k, v)
            for k, v in dict_data.items()
        )
    )
