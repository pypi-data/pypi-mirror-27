"""
Placeholder for future personal library
"""
from elib.custom_logging import get_logger
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

MAIN_LOGGER = get_logger('ELIB')
MAIN_LOGGER.info(f'ELIB version {__version__}')
