from dataclasses import dataclass
from typing import Any


def struct(cls: type[Any]) -> type[Any]:
    return dataclass(frozen=True, slots=True)(cls)


if __name__ == '__main__':
    @struct
    class User:
        id: int
        name: str

    user = User(id=1, name='John')
    print(user)
    print(vars(user))
