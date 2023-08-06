# coding=utf-8
"""
Tests path package
"""

from pathlib import Path

import pytest

import elib.path


def test_path():
    path_str = './test'
    path_test = Path('./test')
    assert elib.path.ensure_path(path_str, must_exit=False) == elib.path.ensure_path(path_test, must_exit=False)
    with pytest.raises(FileNotFoundError):
        elib.path.ensure_path(path_str)
    with pytest.raises(FileNotFoundError):
        elib.path.ensure_path(path_test)
