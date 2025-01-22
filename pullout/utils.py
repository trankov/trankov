from collections.abc import MutableSequence, Sequence
from typing import Any


NonStrSequence = MutableSequence | tuple


class ArgsProcessor:
    def __init__(self, *args):
        self.args = args
        self.prepared_args = []

    def process_square_brackets(self, arg) -> str:
        return (
            arg.replace('[', '.').replace(']', '')
            if '[' in arg and ']' in arg
            else arg
        )

    def process_prefix_dot(self, arg) -> str:
        return arg.removeprefix('.') if arg.startswith('.') else arg

    def process_dots(self, arg) -> str | NonStrSequence:
        return arg.split('.') if '.' in arg else arg

    def string_arg_processing(self, arg) -> str | NonStrSequence:
        steps = (
            self.process_square_brackets,
            self.process_prefix_dot,
            self.process_dots,
        )
        result = arg
        for step in steps:
            result = step(result)
        return result

    def qrow_tail(self, tip) -> None:
        if tip is None:
            return None
        if isinstance(tip, NonStrSequence):
            self.prepared_args.extend(tip)
            return None
        self.prepared_args.append(tip)
        return None

    def prepare(self) -> Sequence[Any]:
        for arg in self.args:
            tip = self.string_arg_processing(arg) if isinstance(arg, str) else arg
            self.qrow_tail(tip)
        return self.prepared_args
