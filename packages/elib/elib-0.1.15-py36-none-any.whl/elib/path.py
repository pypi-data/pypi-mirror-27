# coding=utf-8
"""
Path utilities
"""

import typing
from pathlib import Path


def ensure_path(path: typing.Union[str, Path], must_exit: bool = True) -> Path:
    """
    Ensure path is a Path instance

    Args:
        path: path
        must_exit: if True, raises FileNotFoundError when path does not exist

    Returns: Path instance

    """
    if isinstance(path, str):
        path = Path(path)
    if must_exit and not path.exists():
        raise FileNotFoundError(str(path.absolute()))
    return path
