# coding=utf-8
"""
Utilities to control the console window
"""

import ctypes


def set_title(title: str):
    """
    Sets the console title

    Args:
        title: title as a string
    """
    ctypes.windll.kernel32.SetConsoleTitleW(title)
