import subprocess
from collections.abc import Callable, Sequence
from typing import Any, Self


class PipeReader:
    """
    A class for running a subprocess and sort out it's stdout output on-the-go.

    ```python
    print_ping = PipeReader(
        command=['ping', 'google.com', '-c', '3'],  # command to run
        callback=print, # callback function getting each stdout line as 1st arg
    )
    print_ping(end='')  # pass the arguments for "print" function
    ```

    Fore more control you can process stdout manually without callbacks by using:
    - `PipeReader.popen()` - start a new process
    - `PipeReader.process` - get a process
    - `PipeReader.stdout` - get a line from stdout
    - `PipeReader.stderr` - get a value from stderr
    - `PipeReader.finished` - check if process is finished
    - `PipeReader.running` - check if process is running

    The same example in manual mode:

    ```
    pipe = PipeReader(command=['ping', 'google.com', '-c', '3'])
    while pipe.running:
        print(pipe.stdout, end='')
    pipe.process.terminate()
    ```
    """

    command: Sequence[str]
    callback: Callable[..., Any] | None = None
    _process: subprocess.Popen | None = None

    def __init__(
        self,
        command: Sequence[str],
        callback: Callable[..., Any] | None = None,
    ) -> None:
        self.command = command
        self.callback = callback

    def popen(self) -> Self:
        """Start a new process"""
        self._process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return self

    @property
    def process(self) -> subprocess.Popen:
        if self._process is None:
            self.popen()
        assert self._process is not None, 'Cannot run a given process'
        return self._process

    @property
    def stdout(self) -> str:
        if self.process.stdout is None:
            raise RuntimeError('Process is not running')
        return self.process.stdout.readline()

    @property
    def stderr(self) -> str:
        return '' if self.process.stderr is None else self.process.stderr.read()

    def __del__(self) -> None:
        if self.process is not None:
            self.process.terminate()

    @property
    def finished(self) -> bool:
        if self._process is None:
            return False
        end_of_process_markers = (
            self.process.returncode is not None,
            self.process.poll() is not None,
            self.process.stdout == '',
        )
        return any(end_of_process_markers)

    @property
    def running(self) -> bool:
        return not self.finished

    def __call__(self, *args, **kwargs) -> int | Any:
        if not self.callback:
            raise RuntimeError('Callback is not defined')
        self.popen()  # Запуск процесса (он и так запустится, но лучше явно)
        while self.running:
            self.callback(self.stdout, *args, **kwargs)
        try:
            return self.process.returncode
        finally:
            self.process.terminate()

    def __enter__(self) -> Self:
        self.popen()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            return None
        finally:
            self.process.terminate()


if __name__ == '__main__':
    print_ping = PipeReader(['ping', 'google.com', '-c', '5'], print)
    print_ping(end='')
