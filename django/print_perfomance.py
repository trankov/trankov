"""
Decorate any function and get coloured print
with number of database requests and time spent on it.

"""

from functools import wraps
from time import time

from django.db import connection, reset_queries


def print_perfomance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        t = time()
        out = func(*args, **kwargs)
        t = time() - t
        dashlength = max(41, (len(func.__module__) + len(func.__name__) + 5))
        dashline = "\033[0;34m\N{HORIZONTAL LINE EXTENSION}" * dashlength
        print(
            "\n" + dashline,
            "\033[0;92m"
            + f"{func.__module__} → "
            + "\033[1;32m"
            + f"{func.__name__}()",
            "\t\033[0;96m" + f"{len(connection.queries):<5} request(s)",
            "\t\033[0;36m"
            + f"{sum(float(i['time']) for i in connection.queries):.3f} seconds for queries",
            "\t" + f"{t:.3f} seconds for whole execution",
            dashline,
            "\033[0m",
            sep="\n",
        )
        return out

    return wrapper
