import math
from typing import Self, Sequence


class Pager:
    """
    # A Pager class is a helper for pagination of objects.

    The main goal of this class is to calculate pagination values
    for different usage, like sequence slices or SQL offset/limit pairs.

    You define total number of items and number of items per page
    at initialization. When you change `page` attribute, all values will be
    updated for further usage. The values are:

    - `total_items`: total number of items
    - `page_size`: number of items per page
    - `page`: current page number
    - `pages_count`: total number of pages
    - `offset`: offset for SQL offset/limit pairs
    - `limit`: limit for SQL offset/limit pairs
    - `start`: start index for sequence slices
    - `end`: end index for sequence slices
    - `slicer`: a regular Python slice instance for sequence slices

    Also awailable as properties:

    - `has_prev_page`: is there a previous page
    - `has_next_page`: is there a next page

    It is presumed that all attributes except `page` should be read-only.
    You can try to change them at your own risk, but you don't need it and
    it is not recommended. There is no any protection against it because
    in Python if you want to change some attribute, you'll always find the way.

    It is possible to apply Pager to Python Sequence types for immediate
    slicing. The length of sequence must be equal or greater than `total_items`
    value. If sequence is too short, `ValueError` will be raised.

    Remember that Pager is just a fast calculator of values, for different
    pagination usage. The only aim of this class is to give the proper values
    and to keep a single logic at the different abstraction layers
    (e.g. ORM and Domain models). Once defined, it can be injected into any
    object that can be used for pagination and then provide a correct
    pagination values.

    All syntax sugar here is just a convenience feature, and not for
    conceptual purposes.

    ## Declare Pager

    - `total_items: int` - total number of items
    - `page_size: int` - number of items per page, default is 10

    ```
    >>> pager = Pager(total_items=8, page_size=3)
    ```

    ## Regular usage

    Set `page` attribute to get the bound values

    ```
    >>> pager.page = 3
    >>> pager
    Pager(page=3, pages_count=3, total_items=8, offset=6, limit=3, start=6, end=8)
    ```

    ## Index subscription syntax for page setting

    You can use index subscription syntax to set `page` directly in expression.

    ```
    >>> pager[3]
    Pager(page=3, pages_count=3, total_items=8, offset=6, limit=3, start=6, end=8)
    >>> pager[2].offset, pager[1].end
    (3, 3)
    ```

    ## Using len() for getting pages count

    Instead of getting `pages_count` directly, you can use `len()`
    if it looks more familiar and pythonic for you.

    ```
    >>> len(pager), pager.pages_count
    (3, 3)
    ```

    ## Applying sequence slices

    If your object support slices, you can get [start:end]
    slice using @-sign

    ```
    >>> pager.page = 3
    >>> range(20) @ pager
    range(6, 8)
    >>> range(20) @ pager[1]
    range(0, 3)
    ```

    And, less exotic and more pythonic usage is also possible:

    ```
    >>> pager.page = 2
    >>> list(range(10))[pager.slicer]
    ```

    The `slicer` property is a `slice` object that can be used in `list` and
    other sequence types.

    The difference between `slicer` and @-sign slice is that `slice` object is
    part of Python API and you just send it to any type that supports it. While
    @-sign slice is a function which guarantees that it will be used only with
    sequence types and given sequence have a correct length.

    ## Iterate over pages

    ```
    >>> for page in pager:
    >>>     print(page)
    >>> ...
    Pager(page=1, pages_count=3, total_items=8, offset=0, limit=3, start=0, end=3)
    Pager(page=2, pages_count=3, total_items=8, offset=3, limit=3, start=3, end=6)
    Pager(page=3, pages_count=3, total_items=8, offset=6, limit=3, start=6, end=8)
    >>> [list(range(10)) @ page for page in pager]
    [[0, 1, 2],
    [3, 4, 5],
    [6, 7]]
    ```

    ## Properties usage

    ```
    >>> django_queryset.filter(active=True) @ pager[3]
    >>> ...
    >>> pager.page = 2
    >>> tortoise_queryset.filter(active=True).limit(pager.limit).offset(pager.offset)
    ```

    ## Dict serialization

    Call `state(*args)` method to get dict with pager state values. No args
    returns all values, or you can pass args to get specific values as strings.
    If you pass unknown arg, `AttributeError` will be raised.

    ```
    >>> pager.state("page", "pages_count")
    {'page': 1, 'pages_count': 3}
    >>> pager.state()
    {'page': 1, 'pages_count': 3, 'total_items': 8, 'offset': 0, 'limit': 3, 'start': 0, 'end': 3}
    ```

    It is assumed that basically this feature should be used when generating
    JSON structures in HTTP API responses.
    """

    total_items: int = 0
    page_size: int = 0
    page_num: int = 0
    limit: int = 0
    offset: int = 0
    start: int = 0
    end: int = 0

    def __init__(self, total_items: int, page_size: int) -> None:
        self.total_items = total_items
        self.page_size = page_size
        self.limit = page_size
        self.page_num = 1
        self.set_bounds()

    @property
    def pages_count(self) -> int:
        return math.ceil(self.total_items / self.page_size)

    def set_bounds(self) -> None:
        offset = (self.page_num - 1) * self.page_size
        self.offset = min(offset, self.total_items)
        self.start = offset
        self.end = min(offset + self.page_size, self.total_items)

    @property
    def page(self) -> int:
        return self.page_num

    @page.setter
    def page(self, page: int) -> None:
        if not isinstance(page, int):
            raise TypeError("Page must be an integer")
        page = max(page, 1)
        if page == self.page_num:
            return None
        self.page_num = min(page, self.pages_count)
        self.set_bounds()

    @property
    def slicer(self) -> slice:
        return slice(self.start, self.end)

    def state(self, *args: str) -> dict[str, int]:
        return (
            {arg: getattr(self, arg) for arg in args} if args else {
                "page": self.page,
                "pages_count": self.pages_count,
                "total_items": self.total_items,
                "page_size": self.page_size,
                "offset": self.offset,
                "limit": self.limit,
                "start": self.start,
                "end": self.end,
            }
        )

    @property
    def has_next_page(self) -> bool:
        return self.page < self.pages_count

    @property
    def has_prev_page(self) -> bool:
        return self.page > 1

    def __repr__(self) -> str:
        repr_args = (
            f"page={self.page}",
            f"pages_count={self.pages_count}",
            f"total_items={self.total_items}",
            f"offset={self.offset}",
            f"limit={self.limit}",
            f"start={self.start}",
            f"end={self.end}",
        )
        repr_name = f"{self.__class__.__name__}"
        repr_args_comma = ", ".join(repr_args)
        return f"{repr_name}({repr_args_comma})"

    def __next__(self) -> Self:
        if self.page >= self.pages_count:
            raise StopIteration
        self.page += 1
        return self

    def __iter__(self) -> Self:
        self.page_num = 0
        return self

    def __len__(self) -> int:
        return self.pages_count

    def __getitem__(self, item: int) -> Self:
        self.page = item
        return self

    def __rmatmul__(self, sequence: Sequence) -> Sequence:
        if not isinstance(sequence, Sequence):
            raise TypeError(f"{sequence.__class__!r} not a sequence")
        if len(sequence) < self.total_items:
            raise ValueError("Sequence is too short")
        return sequence[self.start : self.end]
