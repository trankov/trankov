import json
from http import HTTPStatus


class HttpResponceStatus:

    code: int
    phrase: str
    description: str

    def __init__(self, status_code: int):
        # sourcery skip: remove-unnecessary-cast
        try:
            self.code = isinstance(status_code, int) and status_code or int(status_code)
        except (ValueError, TypeError) as err:
            raise ValueError("Cannot cast `status_code` to int") from err
        try:
            http_status = HTTPStatus(status_code)
        except ValueError:
            http_status = None

        if http_status:
            self.phrase = http_status.phrase
            self.description = http_status.description
        else:
            self.phrase = "Unknown status"
            self.description = "Undefined response type"

    def __repr__(self):
        return f"<HttpResponceStatus {self.code}: {self.phrase}>"

    def __str__(self):
        return (f"{self.code}: {self.phrase}. " + (self.description or "")).strip()

    def __int__(self):
        return self.code

    def __abs__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.code == other
        elif isinstance(other, str):
            return (
                (self.code == int(other))
                if other.isdigit()
                else (self.phrase.casefold() == other.casefold())
            )
        else:
            return False

    @property
    def dict(self):
        return {
            "code": self.code,
            "phrase": self.phrase,
            "description": self.description,
        }

    @property
    def json(self):
        return json.dumps(self.dict)

    @property
    def django(self):
        try:
            from django.http import HttpResponse
        except ImportError as err:
            raise RuntimeError("Django not installed") from err
        return type(
            f"HttpResponse{self.code}",
            (HttpResponse,),
            {
                "status_code": self.code,
                "phrase": self.phrase,
                "description": self.description,
            },
        )()