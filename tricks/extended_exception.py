class ExtendedError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message
        self.name = self.__class__.__name__

    def __iter__(self):
        return iter(self.args)

    def __len__(self):
        return len(self.args)

    def __str__(self):
        return f"{self.name}: {self.message}"

    def __repr__(self):
        tb = self.__traceback__
        return (
                f"{self.name} at "
                f"file {tb.tb_frame.f_code.co_filename}, "
                # f"module {tb.tb_frame.f_code.co_name}, "
                f"line {tb.tb_lineno}"
                f": {', '.join(str(i) for i in self.args)}"
            if tb
            else self.__str__()
        )

    def params(self, **kwargs):
        for key, value in kwargs.items():
            if key in ("args", "with_traceback", "message", "name"):
                raise KeyError(f"Key {key} is not allowed")
            setattr(self, key, value)
        return self


class BookingError(ExtendedError):
    pass


class APIError(ExtendedError):
    pass


class WebhookError(ExtendedError):
    pass



if __name__ == "__main__":
    try:
        raise APIError("Message", 404).params(as_json=False)
    except APIError as api_err:
        print(
            api_err,
            f"{api_err.message=}",
            f"{api_err.name=}",
            f"{api_err.as_json=}",
            f"arguments count: {len(api_err)}",
            tuple(api_err),
            sep="\n\t * "
        )
        print(repr(api_err))
