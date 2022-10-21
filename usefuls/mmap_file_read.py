__all__=["fast_file_read"]

from mmap import mmap, ACCESS_READ
from pathlib import Path


def fast_file_read(filepath: Path | str) -> str:
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(filepath)
    with open(filepath, mode="r", encoding="utf8") as fp:
        with mmap(fp.fileno(), length=0, access=ACCESS_READ) as mm_fp:
            mm_fp.seek(0)
            return mm_fp.read().decode("utf-8")
