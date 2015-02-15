__title__ = 'censusname'
__version__ = '0.2.1'
__author__ = 'Neil Freeman'
__license__ = 'GPL'

__all__ = ['censusname', 'formatters']

from .censusname import Censusname, generate, NAMEFILES, SURNAME2000, SURNAME1990, MALEFIRST1990, FEMALEFIRST1990
from . import formatters
