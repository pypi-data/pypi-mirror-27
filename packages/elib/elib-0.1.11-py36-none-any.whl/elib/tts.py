# coding=utf-8
"""
Manages TTS utilities
"""
import typing
from pathlib import Path

import gtts

from elib import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)


def text_to_speech(text: str, file_path: typing.Union[str, Path], overwrite: bool = False) -> Path:
    """
    Creates MP3 file from text

    Args:
        text: text to encode
        file_path: path to MP3 file
        overwrite: whether or not to overwrite existing file

    Returns: path to saved MP3

    """
    LOGGER.debug(f'{text}\n->{file_path}')
    if isinstance(file_path, str):
        LOGGER.debug('converting file path to Path')
        file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        LOGGER.error(f'"{file_path}" already exists')
        raise FileExistsError(file_path)
    LOGGER.debug('encoding text')
    tts = gtts.gTTS(text=text, lang='en', slow=False)
    LOGGER.debug('saving MP3 file')
    tts.save(str(file_path))
    return file_path
